import Papa from "papaparse"

export interface Product {
  id: string;
  name: string;
  category: string;
  rating_mean: number;
  rating_count: number;
  imageURLs: string[];
}

export async function readCSVToJSON(): Promise<Product[]> {
  try {
    const response = await fetch('/data/top3_products.csv');
    const csvText = await response.text();

    const json = Papa.parse(csvText, {header: true})
    const products = json?.data

    return products.map((product: any) => {
        return {
            id: product.asins,
            name: product.name,
            category: product.cluster_name,
            rating_count: product.rating_count,
            rating_mean: parseFloat(product.rating_mean),
            imageURLs: product.imageURLs?.split(",")
        }
    })
  } catch (error) {
    console.error('Fehler beim Lesen der CSV-Datei:', error);
    return [];
  }
}

