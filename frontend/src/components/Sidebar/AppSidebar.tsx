import { BarChart3, Briefcase, Home, Users } from "lucide-react";

import { SidebarAppearance } from "@/components/Common/Appearance";
import { Logo } from "@/components/Common/Logo";
import {
	Sidebar,
	SidebarContent,
	SidebarFooter,
	SidebarHeader,
} from "@/components/ui/sidebar";
import useAuth from "@/hooks/useAuth";
import { type Item, Main } from "./Main";
import { User } from "./User";

/**
 * Build sidebar navigation items based on the current user's role.
 *
 * - admin:   Dashboard, Items, Metrics, Admin
 * - manager: Dashboard, Items, Metrics
 * - member:  Dashboard, Items
 */
function useNavItems(): Item[] {
	const { user: currentUser } = useAuth();

	const items: Item[] = [
		{ icon: Home, title: "Dashboard", path: "/" },
		{ icon: Briefcase, title: "Items", path: "/items" },
	];

	// Admin and Manager can see the Metrics page
	if (currentUser?.role && ["admin", "manager"].includes(currentUser.role)) {
		items.push({ icon: BarChart3, title: "Metrics", path: "/metrics" });
	}

	// Only Admin can see the Admin page
	if (currentUser?.role === "admin") {
		items.push({ icon: Users, title: "Admin", path: "/admin" });
	}

	return items;
}

export function AppSidebar() {
	const items = useNavItems();
	const { user: currentUser } = useAuth();

	return (
		<Sidebar collapsible="icon">
			<SidebarHeader className="px-4 py-6 group-data-[collapsible=icon]:px-0 group-data-[collapsible=icon]:items-center">
				<Logo variant="responsive" />
			</SidebarHeader>
			<SidebarContent>
				<Main items={items} />
			</SidebarContent>
			<SidebarFooter>
				<SidebarAppearance />
				<User user={currentUser} />
			</SidebarFooter>
		</Sidebar>
	);
}

export default AppSidebar;
