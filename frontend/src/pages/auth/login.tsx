import React, { useState } from "react";

const validateEmail = (email: string) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

const Login = () => {
  const [step, setStep] = useState<"email" | "otp">("email");
  const [otp, setOtp] = useState("");
  const [email, setEmail] = useState("");
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

    setErrors(newErrors);

    if (valid) {
      // Proceed to submit the sform or call an API
      // For now just clear errors
      setStep("otp");
    }
  };

  return (
    <div className="w-full h-screen flex gap-4 p-4">
      <div className="w-1/2 h-full rounded-xl bg-[url('/login_bg.jpg')] bg-no-repeat bg-center bg-cover px-6 py-4 hidden lg:flex flex-col justify-between">
        <img src="/logo.png" alt="Logo" className="size-16" />
        <div className="w-full text-white space-y-2">
          <p className="text-sm text-white/70">Seamless access</p>
          <p className="text-4xl font-bold">
            Access your unified academic <br /> dashboard with ease
          </p>
        </div>
      </div>
      <div className="w-full lg:w-1/2 h-full flex flex-col items-center justify-center gap-10">
        <div className="space-y-2 flex justify-center flex-col items-center">
          <img src="/logo_dark.png" alt="Logo" className="size-10" />
          <h3 className="text-xl md:text-3xl font-bold">
            Sign in to your account
          </h3>
          <p className="text-xs md:text-sm md:w-1/2 text-black/40 text-center">
            Use your institutional credentials to securely access all academic
            services and resources
          </p>
        </div>
        <form
          className="w-full md:max-w-1/2 px-6 flex flex-col items-center justify-center"
          onSubmit={handleSubmit}
          noValidate
        >
          <div className="flex flex-col gap-4">
            {step === "email" && (
              <>
                <div>
                  <input
                    type="text"
                    placeholder="Enter your email"
                    className="focus:outline-0 text-xs md:text-sm placeholder:text-black/40 py-2 border border-black/30 rounded-xl px-4 w-full"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </div>

                <button
                  type="submit"
                  className="w-full shadow-xl bg-[#538FA1] text-white py-2 rounded-xl"
                >
                  Send OTP
                </button>
              </>
            )}

            {step === "otp" && (
              <>
                <input
                  type="text"
                  placeholder="Enter OTP"
                  className="focus:outline-0 text-xs md:text-sm py-2 border border-black/30 rounded-xl px-4 w-full"
                  value={otp}
                  onChange={(e) => setOtp(e.target.value)}
                />

                <button
                  type="button"
                  className="w-full shadow-xl bg-[#538FA1] text-white py-2 rounded-xl"
                  onClick={() => {
                    // verify OTP (backend later)

                    // 👇 TEMP redirect (for now)
                    window.location.href = "/student/dashboard";
                  }}
                >
                  Verify OTP
                </button>
              </>
            )}
          </div>
          <div className="flex gap-4 w-full mt-10 items-center justify-center text-black/40">
            <span className="w-full h-1 border-b border-black/20"></span>
            <span className="text-xs w-full whitespace-nowrap">
              or continue with
            </span>
            <span className="w-full h-1 border-b border-black/20"></span>
          </div>

          <button
            onClick={(e) => e.preventDefault()}
            className="w-1/2 lg:w-1/3 cursor-pointer flex items-center justify-center mt-5 bg-black/10 active:bg-black/20 py-2 rounded-xl transition-colors duration-100"
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
