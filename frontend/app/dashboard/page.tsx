"use client"

import { useEffect, useState } from "react"
import { useSession } from "next-auth/react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Play, Clock, Database } from "lucide-react"
import { apiClient, AdminData } from "@/lib/api"
import { toast } from "sonner"
import Image from "next/image"
import zeptoLogo from "@/public/zepto.jpeg"
import swiggyLogo from "@/public/instamart.jpeg"
import blinkitLogo from "@/public/blinkit.png"
import bigbasketLogo from "@/public/bigbasket.jpeg"
import { useRouter } from "next/navigation"

export default function DashboardPage() {
  const { data: session } = useSession()
  const [adminData, setAdminData] = useState<AdminData | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    const fetchAdminData = async () => {
      try {
        setLoading(true)
        const data = await apiClient.getAdminData()
        setAdminData(data)
      } catch (error) {
        toast.error("Failed to fetch admin data")
        console.error(error)
      } finally {
        setLoading(false)
      }
    }

    fetchAdminData()
  }, [])

  const canScrape = (lastScrapeDate: string | null | undefined) => {
    if (!lastScrapeDate) return true
    const lastScrape = new Date(lastScrapeDate)
    const today = new Date()
    const diffTime = Math.abs(today.getTime() - lastScrape.getTime())
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    return diffDays >= 15
  }

  const handleStartScraping = async (platform: string, lastScrapeDate: string | null | undefined) => {
    if (!canScrape(lastScrapeDate)) {
      toast.error(`Cannot scrape ${platform} yet. Please wait 15 days between scrapes.`)
      return
    }

    try {
      let response
      switch (platform) {
        case "zepto":
          response = await apiClient.processZepto()
          break
        case "swiggy":
          response = await apiClient.processSwiggy()
          break
        case "blinkit":
          response = await apiClient.processBlinkit()
          break
        case "bigbasket":
          response = await apiClient.processBigbasket()
          break
        default:
          throw new Error("Invalid platform")
      }

      if (response.status === 200) {
        toast.success(`Started scraping for ${platform}`)
        // Refresh admin data
        const data = await apiClient.getAdminData()
        setAdminData(data)
      }
    } catch (error) {
      toast.error(`Failed to start scraping for ${platform}`)
      console.error(error)
    }
  }

  const formatDate = (dateString: string | null) => {
    if (!dateString) return "Never"
    return new Date(dateString).toLocaleString()
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold">Welcome, {session?.user?.name || "User"}!</h1>
        <p className="text-gray-500">Here's an overview of your scraping dashboard.</p>
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <div className="flex items-center space-x-4">
              <div className="relative h-8 w-8">
                <Image
                  src={zeptoLogo}
                  alt="Zepto"
                  fill
                  className="object-contain"
                />
              </div>
              <div>
                <CardTitle>Zepto</CardTitle>
                <CardDescription>Manage Zepto brand scraping</CardDescription>
              </div>
            </div>
            <div className="flex items-center gap-2 rounded-lg bg-primary/10 px-3 py-1">
              <Database className="h-4 w-4 text-primary" />
              <span className="text-sm font-medium text-primary">
                {adminData?.total_zepto_brands?.toLocaleString() || "0"} brands
              </span>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center gap-2 text-sm text-gray-500">
                <Clock className="h-4 w-4" />
                Last scraped: {adminData ? formatDate(adminData.last_zepto_scrape) : "Loading..."}
              </div>
              <div className="flex gap-2">
                <Button 
                  className="w-1/2 gap-2" 
                  variant="outline"
                  onClick={() => router.push(`/dashboard/zepto`)}
                >
                  <Database className="h-4 w-4" />
                  Browse
                </Button>
                <Button 
                  className="w-1/2 gap-2" 
                  onClick={() => handleStartScraping("zepto", adminData?.last_zepto_scrape)}
                  disabled={loading}
                >
                  <Play className="h-4 w-4" />
                  Start scraping
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <div className="flex items-center space-x-4">
              <div className="relative h-8 w-8">
                <Image
                  src={swiggyLogo}
                  alt="Swiggy"
                  fill
                  className="object-contain"
                />
              </div>
              <div>
                <CardTitle>Swiggy</CardTitle>
                <CardDescription>Manage Swiggy brand scraping</CardDescription>
              </div>
            </div>
            <div className="flex items-center gap-2 rounded-lg bg-primary/10 px-3 py-1">
              <Database className="h-4 w-4 text-primary" />
              <span className="text-sm font-medium text-primary">
                {adminData?.total_swiggy_brands?.toLocaleString() || "0"} brands
              </span>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center gap-2 text-sm text-gray-500">
                <Clock className="h-4 w-4" />
                Last scraped: {adminData ? formatDate(adminData.last_swiggy_scrape) : "Loading..."}
              </div>
              <div className="flex gap-2">
                <Button 
                  className="w-1/2 gap-2" 
                  variant="outline"
                  onClick={() => router.push(`/dashboard/swiggy`)}
                >
                  <Database className="h-4 w-4" />
                  Browse
                </Button>
                <Button 
                  className="w-1/2 gap-2" 
                  onClick={() => handleStartScraping("swiggy", adminData?.last_swiggy_scrape)}
                  disabled={loading}
                >
                  <Play className="h-4 w-4" />
                  Start scraping
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <div className="flex items-center space-x-4">
              <div className="relative h-8 w-8">
                <Image
                  src={blinkitLogo}
                  alt="Blinkit"
                  fill
                  className="object-contain"
                />
              </div>
              <div>
                <CardTitle>Blinkit</CardTitle>
                <CardDescription>Manage Blinkit brand scraping</CardDescription>
              </div>
            </div>
            <div className="flex items-center gap-2 rounded-lg bg-primary/10 px-3 py-1">
              <Database className="h-4 w-4 text-primary" />
              <span className="text-sm font-medium text-primary">
                {adminData?.total_blinkit_brands?.toLocaleString() || "0"} brands
              </span>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center gap-2 text-sm text-gray-500">
                <Clock className="h-4 w-4" />
                Last scraped: {adminData ? formatDate(adminData.last_blinkit_scrape) : "Loading..."}
              </div>
              <div className="flex gap-2">
                <Button 
                  className="w-1/2 gap-2" 
                  variant="outline"
                  onClick={() => router.push(`/dashboard/blinkit`)}
                >
                  <Database className="h-4 w-4" />
                  Browse
                </Button>
                <Button 
                  className="w-1/2 gap-2" 
                  onClick={() => handleStartScraping("blinkit", adminData?.last_blinkit_scrape)}
                  disabled={loading}
                >
                  <Play className="h-4 w-4" />
                  Start scraping
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <div className="flex items-center space-x-4">
              <div className="relative h-8 w-8">
                <Image
                  src={bigbasketLogo}
                  alt="BigBasket"
                  fill
                  className="object-contain"
                />
              </div>
              <div>
                <CardTitle>BigBasket</CardTitle>
                <CardDescription>Manage BigBasket brand scraping</CardDescription>
              </div>
            </div>
            <div className="flex items-center gap-2 rounded-lg bg-primary/10 px-3 py-1">
              <Database className="h-4 w-4 text-primary" />
              <span className="text-sm font-medium text-primary">
                {adminData?.total_bigbasket_brands?.toLocaleString() || "0"} brands
              </span>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center gap-2 text-sm text-gray-500">
                <Clock className="h-4 w-4" />
                Last scraped: {adminData ? formatDate(adminData.last_bigbasket_scrape) : "Loading..."}
              </div>
              <div className="flex gap-2">
                <Button 
                  className="w-1/2 gap-2" 
                  variant="outline"
                  onClick={() => router.push(`/dashboard/bigbasket`)}
                >
                  <Database className="h-4 w-4" />
                  Browse
                </Button>
                <Button 
                  className="w-1/2 gap-2" 
                  onClick={() => handleStartScraping("bigbasket", adminData?.last_bigbasket_scrape)}
                  disabled={loading}
                >
                  <Play className="h-4 w-4" />
                  Start scraping
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
} 