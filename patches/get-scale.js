function get_scale(fileName){
    outlet(0, fileName.split("-scale-")[1].split(".wav")[0])
}