# Set your Cloudinary credentials
# Import the Cloudinary libraries
# ==============================
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Set configuration parameter: return "https" URLs by setting secure=True  
# ==============================
config = cloudinary.config(secure=True)



def uploadImage(imageBLOB):
    imageResponse=cloudinary.uploader.upload(imageBLOB)
    return imageResponse['secure_url']
