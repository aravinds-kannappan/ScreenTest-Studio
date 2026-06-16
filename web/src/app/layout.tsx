import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ScreenTest Studio",
  description: "Screen startup Reels with CrewAI agents before filming.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
