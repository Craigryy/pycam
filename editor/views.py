from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .form import ImageEditForm
from .models import Image, ImageEdit
from .effects import ApplyEffects  
import base64
import os
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import render
from .models import ImageEdit
from django.conf import settings
import json  # Add this import at the top of your views.py

def login(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to the homepage if already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Redirect after successful login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def homepage(request):
    # Query images uploaded by the current user
    images = ImageEdit.objects.filter(user=request.user)
    return render(request, 'homepage.html', {'images': images})


def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        # Assuming you have an ImageEditForm that handles the image
        form = ImageEditForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user  # Associate the image with the user
            image.save()

            # After uploading, redirect to home page
            return redirect('home')
    else:
        form = ImageEditForm()

    return render(request, 'homepage.html', {'form': form})


def delete_image(request, image_id):
    # Fetch the image object to delete, ensuring it's the correct user
    image = get_object_or_404(ImageEdit, id=image_id, user=request.user)
    
    # Delete the image
    image.delete()

    # After deletion, redirect to the home page
    return redirect('home')


def view_image(request, image_id):
    image = get_object_or_404(ImageEdit, id=image_id, user=request.user)
    print(f"Image ID: {image.id}")  # This will show the image ID in the server logs
    return render(request, 'homepage.html', {'image': image})


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)

def feature(request):
    return render(request, 'feature.html')


def custom_logout(request):
    logout(request)
    return redirect('/')  # Redirect to the custom login page


@login_required
def edit_image(request, image_id):
    """View to apply effects to the image."""
    image_instance = get_object_or_404(Image, id=image_id, user=request.user)

    if request.method == 'POST':
        effect = request.POST.get('effect')
        if effect:
            effect_result = ApplyEffects.apply_effect(image_instance.image.path, effect)
            if "applied successfully" in effect_result:
                # Create a new ImageEdit instance for the edited image
                edited_image = image_instance.image.path.replace('images', 'edited')
                edited_instance = ImageEdit(
                    user=request.user,
                    original_image=image_instance.image,
                    edited_image=edited_image,
                    effect_applied=effect
                )
                edited_instance.save()

                # Redirect to the view_image page to display the edited image
                return redirect('view_image', image_id=edited_instance.id)

    # If GET request, show available effects
    effects = ApplyEffects.get_effect_names()
    return render(request, 'edit_image.html', {
        'image': image_instance,
        'effects': effects
    })



from PIL import Image as PILImage
import os
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import JsonResponse
from .models import ImageEdit

def create_thumbnail(image, size=(100, 100)):
    """
    Create a thumbnail for the uploaded image.
    :param image: Image object.
    :param size: Tuple (width, height) for resizing the image.
    :return: Thumbnail image content.
    """
    # Open the image file
    img = PILImage.open(image)
    
    # Resize the image to create a thumbnail
    img.thumbnail(size)
    
    # Save the thumbnail to a memory buffer (instead of saving it directly)
    from io import BytesIO
    thumb_io = BytesIO()
    img.save(thumb_io, 'PNG')
    thumb_io.seek(0)
    
    # Return a ContentFile so it can be saved in the Image model
    return ContentFile(thumb_io.read(), name=f'thumbnails/{os.path.basename(image.name)}')



import json
import base64
import os
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.conf import settings
from PIL import Image as PILImage
from .models import ImageEdit  # Make sure to import the ImageEdit model

def save_edited_image(request):
    if request.method == "POST":
        try:
            # Ensure the user is authenticated
            if not request.user.is_authenticated:
                return JsonResponse({'success': False, 'message': 'User is not authenticated.'})

            # Load the JSON data from the request body
            data = json.loads(request.body)  # Parse the incoming JSON
            image_data = data.get('image_data')

            # Check if the image data is None or empty
            if not image_data:
                return JsonResponse({'success': False, 'message': 'No image data received.'})

            # Log the received image data (for debugging purposes)
            print("Received image data:", image_data[:100])  # Print the first 100 characters

            # Decode the base64 image data
            image_data = image_data.split(';base64,')[1]  # Remove the prefix
            decoded_image = base64.b64decode(image_data)

            # Save the image in the 'edited_images' folder (full-sized image)
            file_name = 'edited_image.png'  # You can customize the file name
            edited_image_path = os.path.join(settings.MEDIA_ROOT, 'edited_images', file_name)

            # Ensure the 'edited_images' directory exists
            os.makedirs(os.path.dirname(edited_image_path), exist_ok=True)

            with open(edited_image_path, 'wb') as f:
                f.write(decoded_image)

            # Create the thumbnail and save it in the 'thumbnails' folder
            thumbnail = create_thumbnail(ContentFile(decoded_image, name=file_name))

            # Save the thumbnail in the 'thumbnails' folder
            thumbnail_file_name = f'thumbnail_{file_name}'
            thumbnail_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', thumbnail_file_name)

            # Ensure the 'thumbnails' directory exists
            os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)

            with open(thumbnail_path, 'wb') as thumb_file:
                thumb_file.write(thumbnail.read())

            # Save the image edit information to the ImageEdit model
            new_image = ImageEdit(
                user=request.user,  # Set the user to the currently logged-in user
                original_image=ContentFile(decoded_image, name=file_name),
                edited_image=ContentFile(decoded_image, name=file_name),  # You can store the edited image here
                effect_applied="Custom Effect",  # Add your actual effect here
            )
            new_image.save()

            return JsonResponse({'success': True, 'message': 'Image and thumbnail saved successfully.'})

        except Exception as e:
            # Log the error and send a response with details
            print("Error saving image:", str(e))
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})
