import fs from "fs";
import path from "path";
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

const INDEX_PATH = path.resolve("search-index.json");
const OUTPUT_PATH = path.resolve("search-index.json");

async function optimizeEntry(entry) {
  const prompt = `
You are optimizing content for:
1. SEO
2. Semantic search accuracy
3. Conversion and monetization

Content:
Title: ${entry.title}
Body: ${entry.content}

Return JSON with:
- seoTitle (max 60 chars)
- seoDescription (max 155 chars)
- keywords (array of strings)
- conversionSummary (short, persuasive summary)
`;

  const response = await client.chat.completions.create({
    model: "gpt-4.1-mini",
    messages: [
      { role: "system", content: "You are an expert SEO + conversion optimizer." },
      { role: "user", content: prompt },
    ],
    temperature: 0.3,
  });

  try {
    return {
      ...entry,
      ...JSON.parse(response.choices[0].message.content),
    };
  } catch {
    return entry;
  }
}

async function run() {
  if (!fs.existsSync(INDEX_PATH)) {
    console.error("❌ search-index.json not found");
    process.exit(1);
  }

  const raw = fs.readFileSync(INDEX_PATH, "utf-8");
  const index = JSON.parse(raw);

  console.log(`🔍 Optimizing ${index.length} index entries with AI...`);

  const optimized = [];
  for (const entry of index) {
    const enriched = await optimizeEntry(entry);
    optimized.push(enriched);
    console.log(`✅ Optimized: ${entry.title}`);
  }

  fs.writeFileSync(OUTPUT_PATH, JSON.stringify(optimized, null, 2));
  console.log("🚀 AI-optimized search index written successfully");
}

run();