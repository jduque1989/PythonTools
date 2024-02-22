#!/bin/bash

# Ask the user for the desired width
read -p "Enter the desired width: " width

# Iterate over all image files in the current directory
for file in *.jpg *.jpeg *.png *.gif; do
    # Check if the file is an image
    if [[ -f $file && $(file -b --mime-type "$file") =~ ^image/ ]]; then
        # Resize the image using the convert command. By specifying only the width,
        # the height is automatically adjusted to maintain the aspect ratio.
        convert "$file" -resize "${width}" "resized_$file" && rm "$file"
        echo "Resized and removed $file"
    fi
done

