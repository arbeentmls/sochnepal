"use client";
import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarHeader,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from "@/components/ui/sidebar";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
    MapPin,
    FileText,
    BarChart3,
    Settings,
    Users,
    HelpCircle,
    LogOut,
    ChevronUp,
    AlertTriangle,
    CheckCircle,
    Clock,
} from "lucide-react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useAuthStore } from "@/store/authStore";
import { toast } from "sonner";

const AppSidebar = () => {
    const pathname = usePathname();
    const router = useRouter();
    const authStore = useAuthStore();

    const mainNavItems = [
        // {
        //     title: "Dashboard",
        //     url: "/dashboard",
        //     icon: Home,
        // },
        // {
        //     title: "Submit Report",
        //     url: "#",
        //     icon: Plus,
        // },
        {
            title: "My Reports",
            url: "/dashboard/my-reports",
            icon: FileText,
        },
        {
            title: "All Reports",
            url: "#",
            icon: MapPin,
        },
    ];

    const reportCategories = [
        {
            title: "Pending",
            url: "#",
            icon: Clock,
            count: 23,
        },
        {
            title: "In Progress",
            url: "#",
            icon: AlertTriangle,
            count: 15,
        },
        {
            title: "Resolved",
            url: "#",
            icon: CheckCircle,
            count: 89,
        },
    ];

    const communityItems = [
        {
            title: "Analytics",
            url: "#",
            icon: BarChart3,
        },
        {
            title: "Community",
            url: "#",
            icon: Users,
        },
    ];

    const supportItems = [
        {
            title: "Help & Support",
            url: "/contact",
            icon: HelpCircle,
        },
        // {
        //     title: "Settings",
        //     url: "#",
        //     icon: Settings,
        // },
    ];

    const handleLogout = () => {
        authStore.logout();
        toast.success("Logged out");
        router.push("/");
    };

    return (
        <Sidebar>
            <SidebarHeader>
                <div className="flex items-center space-x-2 px-4 py-2">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary">
                        <MapPin className="h-5 w-5 text-white" />
                    </div>
                    <span className="text-lg font-bold">SochNepal</span>
                </div>
            </SidebarHeader>

            <SidebarContent>
                {/* Main Navigation */}
                <SidebarGroup>
                    <SidebarGroupLabel>Main</SidebarGroupLabel>
                    <SidebarGroupContent>
                        <SidebarMenu>
                            {mainNavItems.map((item) => (
                                <SidebarMenuItem key={item.title}>
                                    <SidebarMenuButton
                                        asChild
                                        isActive={pathname === item.url}
                                    >
                                        <Link href={item.url}>
                                            <item.icon className="h-4 w-4" />
                                            <span>{item.title}</span>
                                        </Link>
                                    </SidebarMenuButton>
                                </SidebarMenuItem>
                            ))}
                        </SidebarMenu>
                    </SidebarGroupContent>
                </SidebarGroup>

                {/* Report Status */}
                {/* <SidebarGroup>
                    <SidebarGroupLabel>Report Status</SidebarGroupLabel>
                    <SidebarGroupContent>
                        <SidebarMenu>
                            {reportCategories.map((item) => (
                                <SidebarMenuItem key={item.title}>
                                    <SidebarMenuButton
                                        asChild
                                        isActive={pathname.includes(item.url)}
                                    >
                                        <Link href={item.url}>
                                            <item.icon className="h-4 w-4" />
                                            <span>{item.title}</span>
                                            <span className="ml-auto text-xs bg-muted px-2 py-1 rounded-full">
                                                {item.count}
                                            </span>
                                        </Link>
                                    </SidebarMenuButton>
                                </SidebarMenuItem>
                            ))}
                        </SidebarMenu>
                    </SidebarGroupContent>
                </SidebarGroup> */}

                {/* Community */}
                {/* <SidebarGroup>
                    <SidebarGroupLabel>Community</SidebarGroupLabel>
                    <SidebarGroupContent>
                        <SidebarMenu>
                            {communityItems.map((item) => (
                                <SidebarMenuItem key={item.title}>
                                    <SidebarMenuButton
                                        asChild
                                        isActive={pathname === item.url}
                                    >
                                        <Link href={item.url}>
                                            <item.icon className="h-4 w-4" />
                                            <span>{item.title}</span>
                                        </Link>
                                    </SidebarMenuButton>
                                </SidebarMenuItem>
                            ))}
                        </SidebarMenu>
                    </SidebarGroupContent>
                </SidebarGroup> */}

                {/* Support */}
                <SidebarGroup>
                    <SidebarGroupLabel>Support</SidebarGroupLabel>
                    <SidebarGroupContent>
                        <SidebarMenu>
                            {supportItems.map((item) => (
                                <SidebarMenuItem key={item.title}>
                                    <SidebarMenuButton
                                        asChild
                                        isActive={pathname === item.url}
                                    >
                                        <Link href={item.url}>
                                            <item.icon className="h-4 w-4" />
                                            <span>{item.title}</span>
                                        </Link>
                                    </SidebarMenuButton>
                                </SidebarMenuItem>
                            ))}
                        </SidebarMenu>
                    </SidebarGroupContent>
                </SidebarGroup>
            </SidebarContent>

            <SidebarFooter>
                <SidebarMenu>
                    <SidebarMenuItem>
                        <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                                <SidebarMenuButton
                                    size="lg"
                                    className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
                                >
                                    <Avatar className="h-8 w-8 rounded-lg">
                                        <AvatarImage
                                            src=""
                                            alt={authStore.user?.email}
                                        />
                                        <AvatarFallback className="rounded-lg">
                                            {authStore.user?.email?.charAt(0) ||
                                                "U"}
                                        </AvatarFallback>
                                    </Avatar>
                                    {authStore.user && (
                                        <>
                                            <div className="grid flex-1 text-left text-sm leading-tight">
                                                <span className="truncate font-semibold capitalize">
                                                    {`${authStore.user.firstName} ${authStore.user.lastName}`}
                                                </span>
                                                <span className="text-sm font-light">
                                                    {authStore.user.email}
                                                </span>
                                            </div>
                                            <ChevronUp className="ml-auto size-4" />
                                        </>
                                    )}
                                </SidebarMenuButton>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent
                                className="w-[--radix-dropdown-menu-trigger-width] min-w-56 rounded-lg"
                                side="bottom"
                                align="end"
                                sideOffset={4}
                            >
                                <DropdownMenuItem asChild>
                                    <Link href="/dashboard/account-settings">
                                        <Settings className="h-4 w-4 mr-2" />
                                        Account Settings
                                    </Link>
                                </DropdownMenuItem>
                                <DropdownMenuItem asChild>
                                    <Link href="/help">
                                        <HelpCircle className="h-4 w-4 mr-2" />
                                        Support
                                    </Link>
                                </DropdownMenuItem>
                                <DropdownMenuItem onClick={handleLogout}>
                                    <LogOut className="h-4 w-4 mr-2" />
                                    Sign out
                                </DropdownMenuItem>
                            </DropdownMenuContent>
                        </DropdownMenu>
                    </SidebarMenuItem>
                </SidebarMenu>
            </SidebarFooter>
        </Sidebar>
    );
};

export default AppSidebar;
