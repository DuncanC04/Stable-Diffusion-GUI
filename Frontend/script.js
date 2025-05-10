async function generateImage() {
    const prompt = document.getElementById("prompt").value;
    const img = document.getElementById("generatedImage");
    img.style.display = "none";
  
    const response = await fetch("/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ prompt })
    });
  
    const data = await response.json();
    img.src = data.image_url;
    img.style.display = "block";
}
  