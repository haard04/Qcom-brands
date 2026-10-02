import axios from "axios"

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000"

const api = axios.create({
  baseURL: BACKEND_URL,
  headers: {
    "Content-Type": "application/json",
  },
})

export interface Brand {
  id: string
  brand_name: string
  brand_url: string
  brand_created_at: string
}

export interface BrandsResponse {
  brands: Brand[]
}

export interface AdminData {
  user: string
  total_zepto_brands: number
  total_blinkit_brands: number
  total_bigbasket_brands: number
  total_swiggy_brands: number
  last_zepto_scrape: string | null
  last_blinkit_scrape: string | null
  last_bigbasket_scrape: string | null
  last_swiggy_scrape: string | null
}

export const apiClient = {
  // Brand endpoints
  getZeptoBrands: async (): Promise<BrandsResponse> => {
    const response = await axios.get(`${BACKEND_URL}/getZeptoBrands`)
    return response.data
  },

  getSwiggyBrands: async (): Promise<BrandsResponse> => {
    const response = await axios.get(`${BACKEND_URL}/getSwiggyBrands`)
    return response.data
  },

  getBlinkitBrands: async (): Promise<BrandsResponse> => {
    const response = await axios.get(`${BACKEND_URL}/getBlinkitBrands`)
    return response.data
  },

  getBigBasketBrands: async (): Promise<BrandsResponse> => {
    const response = await axios.get(`${BACKEND_URL}/getBigbasketBrands`)
    return response.data
  },

  // Admin endpoints
  getAdminData: async (): Promise<AdminData> => {
    const response = await axios.get(`${BACKEND_URL}/getAdminData`)
    return response.data
  },

  processZepto: async () => {
    return axios.get(`${BACKEND_URL}/processZepto`)
  },

  processSwiggy: async () => {
    return axios.get(`${BACKEND_URL}/processSwiggy`)
  },

  processBlinkit: async () => {
    return axios.get(`${BACKEND_URL}/processBlinkit`)
  },

  processBigbasket: async () => {
    return axios.get(`${BACKEND_URL}/processBigbasket`)
  },

  // Start scraping for a platform
  startScraping: async (platform: string): Promise<void> => {
    await axios.post(`${BACKEND_URL}/scrape/${platform}`)
  }
} 