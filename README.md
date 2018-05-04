# Training an object detection model using Transfer learning with tensorflow and Google collab
This repository train a Mobilenet SSD model pretrained on COCO to detect blackbird.
The annotation process is semi automatic. I am using the base model, that can detect birds in general, to detect the Blackbirds in the imagenet Blackbird repository (~1200 images) and manually approving/rejecting low confidence detections (about a 100).
The resulting CSV is then converted to tfrecord and loaded into collab for transfer training. The resulting Model is downloaded back to the local machine and can be happily used to detect Blackbirds.

# Work in progress!

