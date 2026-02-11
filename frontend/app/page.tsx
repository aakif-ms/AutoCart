"use client";

import { useState } from "react";
import { executeTask, type ProductInput } from "@/services/api";

export default function Home() {
  const [website, setWebsite] = useState("");
  const [products, setProducts] = useState<ProductInput[]>([
    { name: "", max_price: undefined, quantity: 1 },
  ]);
  const [status, setStatus] = useState("");
  const [prompt, setPrompt] = useState("");

  const runAgent = async () => {
    setStatus("Planning and executing task...");
    setPrompt("");

    try {
      const validProducts = products.filter(p => p.name.trim() !== "");

      if (validProducts.length === 0) {
        setStatus("Please add at least one product");
        return;
      }

      const response = await executeTask({
        website,
        products: validProducts,
      });

      setPrompt(response.task_prompt);
      setStatus(`Task started: ${response.execution_status}`);
    } catch (error) {
      console.error("Error executing task:", error);
      setStatus("Error occurred while executing task");
    }
  };

  return (
    <main className="min-h-screen bg-white p-8 text-black">
      {/* Header */}
      <h1 className="text-3xl font-black border-4 border-black inline-block px-6 py-3 mb-8">
        🛒 AutoCart
      </h1>

      {/* Website Input */}
      <div className="mb-8">
        <label className="block font-bold mb-2">Shopping Website</label>
        <input
          className="w-full border-4 border-black px-4 py-2 text-lg focus:outline-none"
          placeholder="amazon.in"
          value={website}
          onChange={(e) => setWebsite(e.target.value)}
        />
      </div>

      {/* Products */}
      <div className="space-y-6">
        {products.map((p, i) => (
          <div
            key={i}
            className="border-4 border-black p-4 space-y-3"
          >
            <h2 className="font-bold">Product {i + 1}</h2>

            {/* Product Name */}
            <input
              className="w-full border-2 border-black px-3 py-2"
              placeholder="Product name"
              value={p.name}
              onChange={(e) => {
                const copy = [...products];
                copy[i].name = e.target.value;
                setProducts(copy);
              }}
            />

            {/* Price + Quantity */}
            <div className="flex gap-4">
              <input
                className="w-1/2 border-2 border-black px-3 py-2"
                placeholder="Max price (₹)"
                type="number"
                value={p.max_price || ""}
                onChange={(e) => {
                  const copy = [...products];
                  copy[i].max_price = e.target.value
                    ? Number(e.target.value)
                    : undefined;
                  setProducts(copy);
                }}
              />

              <input
                className="w-1/2 border-2 border-black px-3 py-2"
                placeholder="Quantity"
                type="number"
                min="1"
                value={p.quantity}
                onChange={(e) => {
                  const copy = [...products];
                  copy[i].quantity = Number(e.target.value) || 1;
                  setProducts(copy);
                }}
              />
            </div>
          </div>
        ))}
      </div>

      {/* Add Product */}
      <button
        onClick={() =>
          setProducts([
            ...products,
            { name: "", max_price: undefined, quantity: 1 },
          ])
        }
        className="mt-6 border-4 border-black px-6 py-2 font-bold hover:bg-black hover:text-white transition"
      >
        + Add Product
      </button>

      {/* Run Agent */}
      <div className="mt-10">
        <button
          onClick={runAgent}
          className="border-4 border-black bg-yellow-300 px-8 py-4 text-xl font-black hover:bg-yellow-400 transition"
        >
          Run Agent
        </button>
      </div>

      {/* Status */}
      {status && (
        <p className="mt-6 font-bold text-lg">{status}</p>
      )}

      {/* Prompt Preview */}
      {prompt && (
        <div className="mt-8">
          <h3 className="font-bold mb-2">Generated Task Prompt</h3>
          <pre className="border-4 border-black p-4 whitespace-pre-wrap text-sm bg-gray-100">
            {prompt}
          </pre>
        </div>
      )}
    </main>
  );
}
