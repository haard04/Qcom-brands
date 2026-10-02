"use client"

import { useEffect, useState } from "react"
import { useParams } from "next/navigation"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { BrandTable } from "@/components/brand-table"
import { apiClient, Brand } from "@/lib/api"
import { toast } from "sonner"
import Image from "next/image"
import zeptoLogo from "@/public/zepto.jpeg"
import swiggyLogo from "@/public/instamart.jpeg"
import blinkitLogo from "@/public/blinkit.png"
import bigbasketLogo from "@/public/bigbasket.jpeg"

const platformEndpoints = {
  zepto: apiClient.getZeptoBrands,
  swiggy: apiClient.getSwiggyBrands,
  blinkit: apiClient.getBlinkitBrands,
  bigbasket: apiClient.getBigBasketBrands,
}

const platformLogos = {
  zepto: zeptoLogo,
  swiggy: swiggyLogo,
  blinkit: blinkitLogo,
  bigbasket: bigbasketLogo,
}

export default function PlatformPage() {
  const params = useParams()
  const platform = params.platform as string
  const [brands, setBrands] = useState<Brand[]>([])
  const [loading, setLoading] = useState(true)

  const platformTitle = platform.charAt(0).toUpperCase() + platform.slice(1)

  useEffect(() => {
    const fetchBrands = async () => {
      try {
        setLoading(true)
        const response = await platformEndpoints[platform as keyof typeof platformEndpoints]()
        setBrands(response.brands)
      } catch (error) {
        toast.error("Failed to fetch brands")
        console.error(error)
      } finally {
        setLoading(false)
      }
    }

    fetchBrands()
  }, [platform])

  const handleFindProducts = async (brandName: string) => {
    toast.info(`Finding products for ${brandName}...`)
    // TODO: Implement product finding logic
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <div className="flex items-center gap-4">
          <div className="relative h-12 w-12">
            <Image
              src={platformLogos[platform as keyof typeof platformLogos]}
              alt={platformTitle}
              fill
              className="object-contain"
            />
          </div>
          <div>
            <h1 className="text-2xl font-bold">{platformTitle} Brands</h1>
            <p className="text-gray-500">Manage and monitor {platformTitle} brand scraping.</p>
          </div>
        </div>
      </div>
      <div className="grid gap-4">
        <Card>
          <CardContent>
            <BrandTable
              brands={brands}
              onFindProducts={handleFindProducts}
              loading={loading}
            />
          </CardContent>
        </Card>
      </div>
    </div>
  )
}