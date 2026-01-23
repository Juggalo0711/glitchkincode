snippets.forEach(file => {
  fetch(file)
    .then(res => res.text())
    .then(data => {
      const div = document.createElement("div");
      div.className = "snippet";
      div.innerHTML = data;
      content.appendChild(div);
    });
});