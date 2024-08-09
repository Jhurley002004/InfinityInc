function removeFlash() {
    // this.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode);
    flashBox = document.getElementById('flash');
    flashBox.parentNode.removeChild(flashBox);
}