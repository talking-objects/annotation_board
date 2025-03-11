
import { Inter } from "next/font/google";
import "./globals.css";
import RecoidContextProvider from "./utils/recoilContextProvider";
import QueryProviderCustom from "./utils/queryClientProvider";


const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Talking Objects Archive",
  description: "Annotation Board",
};

export default function RootLayout({ children }) {
 
  return (
    <html suppressHydrationWarning={true} lang="en">
      <body suppressHydrationWarning={true} className={inter.className}>
        <QueryProviderCustom>
          <RecoidContextProvider>
            {children}
          </RecoidContextProvider>
        </QueryProviderCustom>
      </body>
    </html>
  );
}
