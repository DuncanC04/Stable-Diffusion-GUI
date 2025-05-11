async function generateImage() {
    const prompt = document.getElementById("prompt").value.trim();
    const loading = document.getElementById("loading");
    const resultImage = document.getElementById("resultImage");
  
    if (!prompt) return alert("Please enter a prompt!");
  
    loading.style.display = "block";
    resultImage.src = "";
  
    try {
      const res = await fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
  
      const data = await res.json();
      if (data.image_url) {
        resultImage.src = data.image_url;
      } else {
        alert("Image generation failed.");
      }
    } catch (err) {
      console.error(err);
      alert("Error generating image.");
    } finally {
      loading.style.display = "none";
    }
  }
  