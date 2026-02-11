"use client";

import { useState } from "react";
import { executeTask, type ProductInput } from "@/services/api";

interface ProductFormInput {
  name: string;
  max_price?: number;
  quantity: number | string;
  rating?: string;
}

export default function Home() {
  const [website, setWebsite] = useState("");
  const [products, setProducts] = useState<ProductFormInput[]>([
    { name: "", max_price: undefined, quantity: 1, rating: "" },
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

      // Convert to API format, ensuring quantity is a number
      const apiProducts: ProductInput[] = validProducts.map(p => ({
        name: p.name,
        max_price: p.max_price,
        quantity: typeof p.quantity === 'string' ? parseInt(p.quantity) || 1 : p.quantity,
        rating: p.rating || ""
      }));

      const response = await executeTask({
        website,
        products: apiProducts,
      });

      setPrompt(response.task_prompt);
      setStatus(`Task started: ${response.execution_status}`);
    } catch (error) {
      console.error("Error executing task:", error);
      setStatus("Error occurred while executing task");
    }
  };

  const removeProduct = (index: number) => {
    if (products.length > 1) {
      setProducts(products.filter((_, i) => i !== index));
    }
  };

  return (
    <main className="min-h-screen bg-linear-to-br from-blue-50 via-white to-purple-50 p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-6xl font-black bg-linear-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-4 animate-pulse">
            🛒 AutoCart
          </h1>
          <p className="text-lg md:text-xl text-gray-600 font-medium">
            Automate your shopping with AI-powered cart management
          </p>
        </div>

        <div className="grid gap-8 lg:gap-12">
          <div className="bg-white rounded-2xl shadow-xl border-4 border-purple-200 p-6 md:p-8 hover:shadow-2xl transition-all duration-300 hover:scale-[1.02]">
            <label className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              🌐 Shopping Website
            </label>
            <input
              className="w-full border-3 border-purple-300 rounded-xl px-6 py-4 text-lg focus:outline-none focus:ring-4 focus:ring-purple-200 focus:border-purple-500 transition-all duration-200 bg-gray-50 hover:bg-white text-black"
              placeholder="e.g., amazon.in, flipkart.com"
              value={website}
              onChange={(e) => setWebsite(e.target.value)}
            />
          </div>

          <div className="bg-white rounded-2xl shadow-xl border-4 border-blue-200 p-6 md:p-8 hover:shadow-2xl transition-all duration-300">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
              📦 Products to Purchase
            </h2>
            
            <div className="space-y-6">
              {products.map((p, i) => (
                <div
                  key={i}
                  className="relative bg-linear-to-r from-blue-50 to-purple-50 border-3 border-blue-300 rounded-xl p-6 space-y-4 hover:shadow-lg transition-all duration-200 group"
                >
                  {products.length > 1 && (
                    <button
                      onClick={() => removeProduct(i)}
                      className="absolute top-4 right-4 w-8 h-8 bg-red-500 hover:bg-red-600 text-white rounded-full flex items-center justify-center font-bold text-sm transition-all duration-200 hover:scale-110 opacity-0 group-hover:opacity-100"
                      title="Remove product"
                    >
                      ×
                    </button>
                  )}

                  <div className="flex items-center gap-2 mb-4">
                    <span className="text-lg font-bold text-purple-600">#{i + 1}</span>
                    <h3 className="font-bold text-gray-800">Product {i + 1}</h3>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Product Name</label>
                    <input
                      className="w-full border-2 border-blue-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-200 focus:border-blue-500 transition-all duration-200 bg-white text-black"
                      placeholder="Enter product name..."
                      value={p.name}
                      onChange={(e) => {
                        const copy = [...products];
                        copy[i].name = e.target.value;
                        setProducts(copy);
                      }}
                    />
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-semibold text-gray-700 mb-2">Maximum Price (₹)</label>
                      <input
                        className="w-full border-2 border-green-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-green-200 focus:border-green-500 transition-all duration-200 bg-white text-black"
                        placeholder="Max price"
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
                    </div>

                    <div>
                      <label className="block text-sm font-semibold text-gray-700 mb-2">Quantity</label>
                      <input
                        className="w-full border-2 border-orange-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-orange-200 focus:border-orange-500 transition-all duration-200 bg-white text-black"
                        placeholder="Quantity"
                        type="number"
                        min="1"
                        value={p.quantity || ""}
                        onChange={(e) => {
                          const copy = [...products];
                          const value = e.target.value;
                          if (value === "") {
                            copy[i].quantity = "";
                          } else {
                            const numValue = Number(value);
                            if (numValue > 0) {
                              copy[i].quantity = numValue;
                            }
                          }
                          setProducts(copy);
                        }}
                        onBlur={(e) => {
                          const copy = [...products];
                          const value = e.target.value;
                          if (value === "" || Number(value) < 1) {
                            copy[i].quantity = 1;
                            setProducts(copy);
                          }
                        }}
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-semibold text-gray-700 mb-2">Rating (Optional)</label>
                      <input
                        className="w-full border-2 border-purple-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-200 focus:border-purple-500 transition-all duration-200 bg-white text-black"
                        placeholder="e.g., 4+ stars, good reviews"
                        type="text"
                        value={p.rating || ""}
                        onChange={(e) => {
                          const copy = [...products];
                          copy[i].rating = e.target.value;
                          setProducts(copy);
                        }}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <button
              onClick={() =>
                setProducts([
                  ...products,
                  { name: "", max_price: undefined, quantity: 1, rating: "" },
                ])
              }
              className="mt-6 w-full md:w-auto border-3 border-dashed border-blue-400 bg-blue-50 hover:bg-blue-100 rounded-xl px-8 py-4 font-bold text-blue-700 hover:border-blue-500 transition-all duration-200 flex items-center justify-center gap-2 group"
            >
              <span className="text-2xl group-hover:scale-110 transition-transform">+</span>
              Add Another Product
            </button>
          </div>

          <div className="bg-linear-to-r from-green-400 via-blue-500 to-purple-600 rounded-2xl p-1 shadow-xl hover:shadow-2xl transition-all duration-300">
            <div className="bg-white rounded-xl p-6 md:p-8">
              <div className="text-center">
                <button
                  onClick={runAgent}
                  disabled={!website.trim() || products.every(p => !p.name.trim())}
                  className="relative group disabled:opacity-50 disabled:cursor-not-allowed bg-linear-to-r from-green-500 to-blue-600 hover:from-green-600 hover:to-blue-700 text-white px-12 py-6 text-xl md:text-2xl font-black rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 active:scale-95 disabled:hover:scale-100"
                >
                  <span className="flex items-center gap-3">
                    🚀 Launch AutoCart Agent
                  </span>
                  <div className="absolute inset-0 rounded-2xl bg-linear-to-r from-yellow-400 to-pink-500 opacity-0 group-hover:opacity-20 transition-opacity duration-300"></div>
                </button>
                {(!website.trim() || products.every(p => !p.name.trim())) && (
                  <p className="text-sm text-gray-500 mt-3">
                    Please enter a website and at least one product name to continue
                  </p>
                )}
              </div>
            </div>
          </div>

          {status && (
            <div className={`rounded-2xl p-6 border-l-4 ${
              status.includes("Error") 
                ? "bg-red-50 border-red-500 text-red-800" 
                : status.includes("started")
                ? "bg-green-50 border-green-500 text-green-800"
                : "bg-blue-50 border-blue-500 text-blue-800"
            } shadow-lg animate-fade-in`}>
              <div className="flex items-center gap-3">
                <div className="w-3 h-3 rounded-full bg-current animate-pulse"></div>
                <p className="font-bold text-lg">{status}</p>
              </div>
            </div>
          )}

          {prompt && (
            <div className="bg-white rounded-2xl shadow-xl border-4 border-gray-200 p-6 md:p-8 hover:shadow-2xl transition-all duration-300">
              <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                📋 Generated Task Prompt
              </h3>
              <div className="bg-gray-50 border-2 border-gray-200 rounded-xl p-6 max-h-96 overflow-y-auto">
                <pre className="whitespace-pre-wrap text-sm text-gray-700 leading-relaxed font-mono">
                  {prompt}
                </pre>
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
