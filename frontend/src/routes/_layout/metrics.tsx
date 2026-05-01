import { createFileRoute, redirect } from "@tanstack/react-router"
import { UsersService } from "@/client"
import useAuth from "@/hooks/useAuth"

export const Route = createFileRoute("/_layout/metrics")({
  component: Metrics,
  beforeLoad: async () => {
    // Fetch current user to check role before rendering
    const user = await UsersService.readUserMe()
    if (!user.role || !["admin", "manager"].includes(user.role)) {
      throw redirect({
        to: "/access-denied",
      })
    }
  },
  head: () => ({
    meta: [
      {
        title: "Metrics - FastAPI Template",
      },
    ],
  }),
})

function Metrics() {
  const { user: currentUser } = useAuth()

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">
          Metrics & Insights
        </h1>
        <p className="text-muted-foreground">
          Application metrics and usage insights.
          {currentUser?.role === "manager" && (
            <span className="ml-2 text-xs">(View only)</span>
          )}
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        {/* Metric card: Total Users */}
        <div className="rounded-lg border bg-card p-6 text-card-foreground shadow-sm">
          <p className="text-sm font-medium text-muted-foreground">
            Total Users
          </p>
          <p className="text-3xl font-bold">—</p>
          <p className="text-xs text-muted-foreground mt-1">
            Connect to your data source
          </p>
        </div>

        {/* Metric card: Active Users */}
        <div className="rounded-lg border bg-card p-6 text-card-foreground shadow-sm">
          <p className="text-sm font-medium text-muted-foreground">
            Active Users
          </p>
          <p className="text-3xl font-bold">—</p>
          <p className="text-xs text-muted-foreground mt-1">
            Connect to your data source
          </p>
        </div>

        {/* Metric card: Total Items */}
        <div className="rounded-lg border bg-card p-6 text-card-foreground shadow-sm">
          <p className="text-sm font-medium text-muted-foreground">
            Total Items
          </p>
          <p className="text-3xl font-bold">—</p>
          <p className="text-xs text-muted-foreground mt-1">
            Connect to your data source
          </p>
        </div>
      </div>

      <div className="rounded-lg border bg-card p-6 text-card-foreground shadow-sm">
        <h2 className="text-lg font-semibold mb-2">Insights</h2>
        <p className="text-muted-foreground text-sm">
          This is a stub page. In a production application, this would display
          real-time metrics, charts, and usage analytics powered by your data
          layer.
        </p>
      </div>
    </div>
  )
}
