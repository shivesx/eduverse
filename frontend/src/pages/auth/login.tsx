import { EyeClosed, Eye } from "lucide-react";
import React, { useState } from "react";

const validateEmail = (email: string) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

const Login = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState<{ email?: string; password?: string }>(
    {},
  );

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    let valid = true;
    const newErrors: { email?: string; password?: string } = {};

    if (!email) {
      newErrors.email = "Email is required";
      valid = false;
    } else if (!validateEmail(email)) {
      newErrors.email = "Enter a valid email";
      valid = false;
    }

    if (!password) {
      newErrors.password = "Password is required";
      valid = false;
    }

    setErrors(newErrors);

    if (valid) {
      // Proceed to submit the form or call an API
      // For now just clear errors
    }
  };

  return (
    <div className="w-full h-full flex gap-4 p-4">
      <div className="w-1/2 h-full rounded-xl bg-[url('/login_bg.jpg')] bg-no-repeat bg-center bg-cover px-6 py-4 flex flex-col justify-between">
        <img src="/logo.png" alt="Logo" className="size-16" />
        <div className="w-full text-white space-y-2">
          <p className="text-sm text-white/70">Seamless access</p>
          <p className="text-4xl font-bold">
            Access your unified academic <br /> dashboard with ease
          </p>
        </div>
      </div>
      <div className="w-1/2 h-full flex flex-col items-center justify-center gap-10">
        <div className="space-y-2 flex justify-center flex-col items-center">
          <img src="/logo_dark.png" alt="Logo" className="size-10" />
          <h3 className="text-3xl font-bold">Sign in to your account</h3>
          <p className="text-sm text-black/40 w-1/2 text-center">
            Use your institutional credentials to securely access all academic
            services and resources
          </p>
        </div>
        <form
          className="w-full max-w-1/2 px-6 flex flex-col items-center justify-center"
          onSubmit={handleSubmit}
          noValidate
        >
          <div className="flex flex-col gap-4">
            <div>
              <input
                type="text"
                placeholder="Enter your email"
                className="focus:outline-0 placeholder:text-sm placeholder:text-black/40 py-2 border border-black/30 rounded-xl px-4 w-full"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                aria-invalid={!!errors.email}
                aria-describedby={errors.email ? "email-error" : undefined}
                autoComplete="email"
              />
              {errors.email && (
                <p
                  id="email-error"
                  className="text-xs text-red-500 mt-1 ml-4"
                  role="alert"
                >
                  {errors.email}
                </p>
              )}
            </div>
            <div>
              <span className="relative w-full block">
                <input
                  type={showPassword ? "text" : "password"}
                  placeholder="Enter your password"
                  className="focus:outline-0 placeholder:text-sm placeholder:text-black/40 py-2 border border-black/30 rounded-xl px-4 pr-22 w-full"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  aria-invalid={!!errors.password}
                  aria-describedby={
                    errors.password ? "password-error" : undefined
                  }
                  autoComplete="current-password"
                />
                <button
                  type="button"
                  onClick={(e) => {
                    e.preventDefault();
                    setShowPassword((prev) => !prev);
                  }}
                  className="text-black/50 absolute right-3 top-1/2 -translate-y-1/2 p-0 m-0 bg-transparent border-none outline-none flex items-center justify-center cursor-pointer"
                  aria-label={showPassword ? "Hide password" : "Show password"}
                  tabIndex={-1}
                >
                  {showPassword ? <EyeClosed size={18} /> : <Eye size={18} />}
                </button>
              </span>
              {errors.password && (
                <p
                  id="password-error"
                  className="text-xs text-red-500 mt-1 ml-4"
                  role="alert"
                >
                  {errors.password}
                </p>
              )}

              <p className="text-sm underline text-black/30 text-right mt-1 cursor-pointer">
                <a href="#">Forgot Password?</a>
              </p>
            </div>
            <button
              type="submit"
              className="w-full shadow-xl bg-[#538FA1] active:bg-[#3D7A8F] text-white py-2 rounded-xl cursor-pointer transition-colors duration-100"
            >
              Login
            </button>
          </div>
          <div className="flex gap-4 w-full mt-10 items-center justify-center text-black/40">
            <span className="w-full h-1 border-b border-black/20"></span>
            <span className="text-xs w-full">or continue with</span>
            <span className="w-full h-1 border-b border-black/20"></span>
          </div>

          <button
            onClick={(e) => e.preventDefault()}
            className="w-1/3 cursor-pointer flex items-center justify-center mt-5 bg-black/10 active:bg-black/20 py-2 rounded-xl transition-colors duration-100"
            type="button"
          >
            <img src="/google_logo.png" alt="Google Logo" className="size-5" />
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
