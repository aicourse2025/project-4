import { useEffect, useState } from "react";
import StarRating from "./components/StarRating";
import ProgressiveImage from "./components/ProgressiveImage";
import { generateFinalSummary, generateProductSummary } from "./axios";
import { readCSVToJSON, type Product } from "./helper/csv";
import ReactMarkdown from "react-markdown";

function App() {
  const cards = [
    {
      title: "Entertainment Tablets",
      image: "/images/cat1.png",
      description: "Tablets ideal for gaming, streaming, and multimedia consumption.",
    },
    {
      title: "E-Reader & Office Tablets",
      image: "/images/cat2.png",
      description: "Devices perfect for reading eBooks and handling office tasks efficiently.",
    },
    {
      title: "Health & household accessories",
      image: "/images/cat3.png",
      description: "Essential accessories for health monitoring and home care.",
    },
    {
      title: "Smart Home & Amazon devices",
      image: "/images/cat4.png",
      description: "Smart home devices and Alexa-enabled products.",
    },
  ];

  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [topProducts, setTopProducts] = useState<Product[]>([])
  const [categoryProducts, setCategoryProducts] = useState<Product[]>([])

  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [loading1, setLoading1] = useState(true)
  const [loading2, setLoading2] = useState(true)
  const [loading3, setLoading3] = useState(true)
  const [loading4, setLoading4] = useState(false)

  const [error1, setError1] = useState(false)
  const [error2, setError2] = useState(false)
  const [error3, setError3] = useState(false)

  const [summary1, setSummary1] = useState("");
  const [summary2, setSummary2] = useState("");
  const [summary3, setSummary3] = useState("");
  const [finalSummary, setFinalSummary] = useState("")

  useEffect(() => {
    async function fetchData() {
      const res = await readCSVToJSON()
      setTopProducts(res)
    }

    void fetchData()
  }, [])

  useEffect(() => {
    if (selectedCategory) {
      setCategoryProducts(topProducts.filter(p => p.category === selectedCategory))
    }
  }, [selectedCategory])

  const handleGenerateSummary = async () => {
    setIsDialogOpen(true)

    try {
      const [result1, result2, result3] = await Promise.all([
        generateProductSummary(categoryProducts[0].id).catch(() => setError1(true)).finally(() => setLoading1(false)),
        generateProductSummary(categoryProducts[1].id).catch(() => setError2(true)).finally(() => setLoading2(false)),
        generateProductSummary(categoryProducts[2].id).catch(() => setError3(true)).finally(() => setLoading3(false)),
      ]);
  
      setSummary1(result1.generated_text);
      setSummary2(result2.generated_text);
      setSummary3(result3.generated_text);
    } catch (e) {
      console.error(e)
    }
  }

  useEffect(() => {
    if (summary1 && summary2 && summary3) {
      async function fetchData() {
        setLoading4(true)

        const res = await generateFinalSummary(selectedCategory || "", [summary1, summary2, summary3])

        setLoading1(true)
        setLoading2(true)
        setLoading3(true)
        setLoading4(false)

        setSummary1("")
        setSummary2("")
        setSummary3("")
        
        setFinalSummary(res?.generated_text)
      }
     
      void fetchData()
    }

  }, [summary1, summary2, summary3])

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center py-10">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6 max-w-6xl w-full px-4">
        {cards.map(({ title, image, description }) => (
          <div
            key={title}
            onClick={() => setSelectedCategory(title)}
            className={`cursor-pointer bg-white rounded-lg shadow-md overflow-hidden flex flex-col
              hover:shadow-xl transition-shadow duration-300
              ${selectedCategory === title ? "ring-4 ring-blue-400" : ""}
            `}
          >
            <img
              src={image}
              alt={title}
              className="w-full h-40 object-cover rounded-t-lg mb-4"
            />
            <h2 className="text-lg font-semibold px-4">{title}</h2>
            <p className="text-gray-600 px-4">{description}</p>
          </div>
        ))}
      </div>

      {selectedCategory !== null && (
        <div className="mt-12 w-full max-w-6xl px-4">
          <h2 className="text-2xl font-bold mb-6">{selectedCategory} (Top-3 products)</h2>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            {categoryProducts.map(({ id, name, imageURLs, rating_mean, rating_count }) => (
              <div key={id} className="bg-white rounded-lg shadow-md p-4 flex flex-col">
                <ProgressiveImage imageURLs={imageURLs} placeholder="/images/placeholder.png"/>
                <h3 className="text-md font-semibold">{name}</h3>
                <StarRating rating={rating_mean} />
                <p className="text-sm text-gray-700 mt-1">
                  <span className="font-semibold">{rating_mean}</span> ({rating_count} reviews)
                </p>
              </div>
            ))}
          </div>

          <div className="flex justify-center mt-12">
            <button
              onClick={handleGenerateSummary}
              className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 transition cursor-pointer"
            >
              Generate summary and recommendation
            </button>
          </div>
        </div>
      )}

      {isDialogOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg shadow-lg p-6 max-w-2xl max-h-[80vh] overflow-y-auto">
              {!finalSummary ? (
                <>
                <h3 className="text-xl font-bold mb-4">AI is generating...</h3>
                <div className="flex items-center space-x-4 mb-4">
                  {loading1 ? (<div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-500"></div>) : <div className="w-5">{!error1 ? "✅" : "❌"}</div>}
                  <span className="text-gray-600">Summary of the first product</span>
                </div>
                <div className="flex items-center space-x-4 mb-4">
                  {loading2 ? (<div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-500"></div>) : <div className="w-5">{!error2 ? "✅" : "❌"}</div>}
                  <span className="text-gray-600">Summary of the second product</span>
                </div>
                <div className="flex items-center space-x-4 mb-4">
                  {loading3 ? (<div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-500"></div>) : <div className="w-5">{!error3 ? "✅" : "❌"}</div>}
                  <span className="text-gray-600">Summary of the third product</span>
                </div>
                <div className="flex items-center space-x-4 mb-4">
                  {loading4 ? (<div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-500"></div>) : <div className="w-5"></div>}
                  <span className="text-gray-600">Final summary and recommendation</span>
                </div>
                </>
              ) : (
                <>
                  <h3 className="text-xl font-bold mb-4">LLM: Meta Llama 3.1 8B instruct</h3>
                  <ReactMarkdown
  components={{
    h1: ({ node, ...props }) => (
      <h1 className="text-4xl font-bold my-4" {...props} />
    ),
    h2: ({ node, ...props }) => (
      <h2 className="text-3xl font-semibold my-3" {...props} />
    ),
    h3: ({ node, ...props }) => (
      <h3 className="text-2xl font-medium my-2" {...props} />
    ),
    p: ({ node, ...props }) => (
      <p className="text-base leading-relaxed my-2" {...props} />
    ),
    ul: ({ node, ...props }) => (
      <ul className="list-disc list-inside my-2 pl-4" {...props} />
    ),
    ol: ({ node, ...props }) => (
      <ol className="list-decimal list-inside my-2 pl-4" {...props} />
    ),
    li: ({ node, ...props }) => (
      <li className="mb-1" {...props} />
    ),
    a: ({ node, ...props }) => (
      <a className="text-blue-600 hover:underline" {...props} />
    ),
    blockquote: ({ node, ...props }) => (
      <blockquote className="border-l-4 border-gray-300 pl-4 italic text-gray-600 my-4" {...props} />
    ),
  }}
>
  {finalSummary}
</ReactMarkdown>

                </>
              )}

            {finalSummary && (
              <div className="flex justify-end mt-6">
              <button
                onClick={() => {
                  setIsDialogOpen(false)
                  setFinalSummary("")
                }}
                className="bg-gray-300 px-4 py-2 rounded hover:bg-gray-400 cursor-pointer"
              >
                Close
              </button>
              </div>
            )}
           
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
