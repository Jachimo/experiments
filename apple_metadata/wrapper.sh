# Sample wrapper script for set_color_sidecar
# Usage:
#    poetry install
#    cp wrapper.sh /path/to/macos/files
#    cd /path/to/macos/files
#    ./wrapper.sh

N=12  # Spawn 12 simultaneous instances of the program (and its subshells!)
(
for f in *.{jpg,m4v,bmp,mp4,mkv,mov,png,avi,mrw,jpeg}; do 
    set_color_sidecar "$f" &  
done
) && echo "Wrapper script complete"
