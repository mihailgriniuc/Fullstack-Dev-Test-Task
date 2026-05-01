import { Link } from "@tanstack/react-router";
import { Button } from "@/components/ui/button";

/**
 * AccessDenied — shown when a user navigates to a page they don't have
 * permission to access. Provides a clear message and a way back home.
 */
const AccessDenied = () => {
	return (
		<div className="flex min-h-screen items-center justify-center flex-col p-4">
			<div className="flex items-center z-10">
				<div className="flex flex-col ml-4 items-center justify-center p-4">
					<span className="text-6xl md:text-8xl font-bold leading-none mb-4">
						403
					</span>
					<span className="text-2xl font-bold mb-2">Access Denied</span>
				</div>
			</div>

			<p className="text-lg text-muted-foreground mb-4 text-center z-10">
				You don't have permission to access this page. If you believe this is a
				mistake, contact your administrator.
			</p>
			<div className="z-10">
				<Link to="/">
					<Button className="mt-4">Go Home</Button>
				</Link>
			</div>
		</div>
	);
};

export default AccessDenied;
