async function loadImages() {
    const res = await fetch("http://localhost:8000/generate");
    const data = await res.json();
    const container = document.getElementById("images");
    container.innerHTML = "";
  
    data.images.forEach(img => {
      const image = document.createElement("img");
      image.src = `data:image/png;base64,${img.data}`;
      image.dataset.id = img.id;
  
      image.onclick = () => {
        document.querySelectorAll("img").forEach(el => el.classList.remove("selected"));
        image.classList.add("selected");
        selectImage(img.id);
      };
  
      container.appendChild(image);
    });
  }
  
  async function selectImage(id) {
    await fetch("http://localhost:8000/select", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ selected_id: id })
    });
  
    console.log("Selected image cached:", id);
  }
  
  loadImages();
  