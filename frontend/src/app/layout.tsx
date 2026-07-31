import "./globals.css";
import Sidebar from "@/components/Sidebar";
import Navbar from "@/components/Navbar";
import AuthGuard from "@/components/AuthGuard";

export const metadata = {
  title: "PhishGuard AI - Production AI Phishing Detection System",
  description: "Enterprise multi-vector phishing detection platform powered by Machine Learning and Google Gemini AI.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="bg-[#090d16] text-slate-100 antialiased min-h-screen flex" suppressHydrationWarning>
        <Sidebar />
        <div className="flex-1 flex flex-col min-w-0">
          <Navbar />
          <main className="p-6 md:p-8 flex-1 max-w-7xl w-full mx-auto">
            <AuthGuard>
              {children}
            </AuthGuard>
          </main>
        </div>
      </body>
    </html>
  );
}
