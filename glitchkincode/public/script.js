document.getElementById("year").textContent = new Date().getFullYear();

// Example: replace with your own data (could be fetched or inlined)
const content = {
  headline: "Glitchkin Code",
  subhead: "Describe what you build, who it helps, and why it matters.",
  ctaPrimary: "See the Demo",
  ctaSecondary: "Contact",
};

document.getElementById("headline").textContent = content.headline;
document.getElementById("subhead").textContent = content.subhead;
document.getElementById("cta-button").textContent = content.ctaPrimary;
document.getElementById("cta-button-secondary").textContent = content.ctaSecondary;
