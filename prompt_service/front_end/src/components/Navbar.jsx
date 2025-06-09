import { Link } from "react-router-dom";
import logo from "../assets/Logo_HUET.png"; // Nếu bạn muốn thêm logo thật sự

export default function Navbar() {
  return (
    <nav className="bg-blue-800 text-white px-6 py-3 shadow-md">
      <div className="max-w-7xl mx-auto flex items-center">
        {/* Logo + Tên trường */}
        <div className="flex items-center space-x-3 flex-1">
          {/* Bật logo nếu bạn muốn */}
          {/* <img src={logo} alt="UET" className="h-10" /> */}
          <span className="font-semibold text-sm md:text-base lg:text-lg leading-snug">
            VNU University of Engineering and Technology – Vietnam National University
          </span>
        </div>

        {/* Menu bên phải */}
        <div className="space-x-8 text-sm font-medium">
          <Link to="/" className="hover:underline">
            Trang chủ
          </Link>
          <Link to="/history" className="hover:underline">
            Lịch sử trò chuyện
          </Link>
          <Link to="/profile" className="hover:underline">
            Tài khoản
          </Link>
        </div>
      </div>
    </nav>
  );
}
