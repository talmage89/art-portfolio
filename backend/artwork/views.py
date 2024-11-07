from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Artwork, Image
from .serializers import ArtworkSerializer, ImageSerializer


class ArtworkViewSet(viewsets.ModelViewSet):
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer
    parser_classes = (MultiPartParser, FormParser)  # To handle image uploads

    def perform_create(self, serializer):
        # Optionally handle image creation alongside artwork
        artwork = serializer.save()
        # You can add any additional logic here for handling image uploads
        # (e.g., associating images with artwork)
        # Example: associate an image to the artwork after it's created
        if "image" in self.request.FILES:
            Image.objects.create(artwork=artwork, image=self.request.FILES["image"])


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)
