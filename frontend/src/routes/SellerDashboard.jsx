import Sidebar from "../components/Seller/Sidebar";
import Header from "../components/Seller/Header";
import MainContent from "../components/Seller/MainContent";

export default function SellerDashboard() {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex flex-col flex-1">
        <Header />
        <MainContent />
      </div>
    </div>
  );
}