#!/usr/bin/env bash
#  Script to batch convert videos in a directory tree to H.265 using hardware acceleration if available.
#  Version 1.0 - 2025-10-12
#  Currently only tested on NVIDIA GPU

INPUT_EXTENSION=".dv"
OUTPUT_EXTENSION=".mov"

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "ffmpeg could not be found"
    exit 1
fi

# Detect GPU type and set appropriate encoder
GPU_ENCODER=""
if command -v nvidia-smi &> /dev/null && nvidia-smi &> /dev/null; then
    GPU_ENCODER="hevc_nvenc"
    PIXFMT="nv12"
    echo "NVIDIA GPU detected, using hevc_nvenc encoder and $PIXFMT pixel format"
elif lspci | grep -i "amd\|ati" &> /dev/null; then
    GPU_ENCODER="hevc_amf"
    PIXFMT="yuv420p"
    echo "AMD GPU detected, using hevc_amf encoder and $PIXFMT pixel format"
elif lspci | grep -i "intel" &> /dev/null; then
    GPU_ENCODER="hevc_qsv"
    PIXFMT="yuv420p"
    echo "Intel GPU detected, using hevc_qsv encoder and $PIXFMT pixel format"
else
    GPU_ENCODER="libx265"
    PIXFMT="yuv420p"
    echo "No compatible GPU detected, falling back to software H.265 encoder (libx265) and $PIXFMT pixel format"
fi

find . -type f -name "*$INPUT_EXTENSION" -print0 | while IFS= read -r -d '' file; do
    INFILE="$file"
    OUTFILE="${file%$INPUT_EXTENSION}$OUTPUT_EXTENSION"

    echo "Converting '$file' to '$OUTFILE'"

    if [ -f "$OUTFILE" ]; then
        echo "Output file '$OUTFILE' already exists, skipping"
        continue
    fi

    ffmpeg -hide_banner -nostdin \
    -i "$file" \
    -pix_fmt "$PIXFMT" \
    -r 30 \
    -c:v "$GPU_ENCODER" -preset medium \
    -c:a copy \
    "$OUTFILE"
done
