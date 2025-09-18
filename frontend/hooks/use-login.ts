import { customAxios } from "@/lib/customAxios";
import { useAuthStore } from "@/store/authStore";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";

export const loginSchema = z.object({
    email: z.string().email("Please enter a valid email address"),
    password: z.string().min(8, "Password must be at least 8 characters"),
});

export const useLogin = () => {
    const form = useForm<z.infer<typeof loginSchema>>({
        resolver: zodResolver(loginSchema),
        defaultValues: {
            email: "",
            password: "",
        },
    });

    const router = useRouter();
    const authStore = useAuthStore();
    const { mutate, isPending } = useMutation({
        mutationFn: async (data: z.infer<typeof loginSchema>) => {
            const response = await customAxios.post("/auth/jwt/cookie/", {
                email: data.email,
                password: data.password,
            });
            return response.data;
        },
        onSuccess: () => {
            authStore.login({
                email: form.getValues("email"),
                firstName: "",
                lastName: "",
                is_verified: false,
            });
            toast.success("Logged in successfully");
            router.push("/dashboard/my-reports");
            form.reset();
        },
        onError: (error) => {
            if (axios.isAxiosError(error)) {
                if (error.status === 401) {
                    toast.error("Invalid credentials", {
                        description:
                            "Your email or password does not match. Please try again",
                    });
                    return;
                }
            }
            toast.error("Something went wrong", {
                description: "Could not process your request. Please try again",
            });
        },
    });
    return { mutate, isPending, form };
};
