import { yupResolver } from "@hookform/resolvers/yup";
import { useCallback, useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import * as Yup from "yup";

import { mutationApi } from "../../hooks/useApi";

const validationSchema = Yup.object().shape({
  username: Yup.string()
    .min(3, "Username must be at least 3 characters")
    .max(20, "Username cannot be longer than 20 characters")
    .matches(/^[a-zA-Z0-9]+$/, "Username can only contain letters and numbers")
    .required("Username is required"),

  email: Yup.string()
    .email("Invalid email format")
    .required("Email is required"),

  password: Yup.string()
    .min(8, "Password must be at least 8 characters")
    .matches(/[a-z]/, "Password must contain at least one lowercase letter")
    .matches(/[A-Z]/, "Password must contain at least one uppercase letter")
    .matches(/\d/, "Password must contain at least one number")
    .matches(
      /[!@#$%^&*(),.?":{}|<>]/,
      "Password must contain at least one special character"
    )
    .required("Password is required"),

  cPassword: Yup.string()
    .oneOf([Yup.ref("password"), null], "Passwords must match")
    .required("Confirm password is required"),
});

function SignupPage() {
  const navigate = useNavigate();

  const [formStep, setFormStep] = useState(1);
  const totalSteps = 3;

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
    trigger,
    watch,
  } = useForm({
    resolver: yupResolver(validationSchema),
    mode: "onChange",
  });

  const handleFormSubmission = async (data) => {
    if (formStep === totalSteps) {
      // eslint-disable-next-line no-unused-vars
      const { cPassword, ...formData } = data;
      const result = await mutationApi("/auth/sign-up", formData);
      if (result?.success) {
        console.log(result);
        navigate("/auth/login");
      }
    }
  };

  const nextStep = useCallback(async () => {
    const fields = ["username", "email", "password", "cPassword"];
    const isStepValid = await trigger(fields[formStep - 1]);

    if (isStepValid) {
      setFormStep((currentStep) => {
        const nextStep = Math.min(currentStep + 1, totalSteps);
        return nextStep;
      });
    }
  }, [formStep, trigger, totalSteps]);

  const prevStep = useCallback(() => {
    setFormStep((currentStep) => Math.max(currentStep - 1, 1));
  }, []);

  // Write a function to to validate each step before clicking on the next button
  const isStepValid = useCallback(() => {
    const fields = ["username", "email", "password"];
    const currentField = fields[formStep - 1];
    return !errors[currentField] && watch(currentField);
  }, [errors, formStep, watch]);

  return (
    <div className="flex items-center justify-center flex-1">
      <div className="w-[60%] flex flex-col gap-6">
        <div className="flex flex-col items-center">
          <h2 className="text-2xl font-bold text-violet-300">
            Create your account on Textify! 👋🏻
          </h2>
          <p className="mt-3 text-sm leading-6 text-center text-neutral-300">
            Stay connected with the people who matter. Sign up now to start
            chatting effortlessly!
          </p>
        </div>

        <form onSubmit={handleSubmit(handleFormSubmission)}>
          {formStep === 1 && (
            <div className="relative space-y-2">
              <label
                htmlFor="username"
                className="block text-sm text-neutral-300"
              >
                Username
              </label>
              <input
                type="text"
                id="username"
                {...register("username")}
                placeholder="johndoe02"
                className="w-full px-4 py-2 text-sm bg-transparent border rounded-md text-zinc-300 placeholder:text-zinc-400 focus:outline-1 border-neutral-400 focus:outline-offset-[3px] focus:ring-0"
              />
              {errors.username && (
                <small className="absolute block !mt-3 text-red-400">
                  {errors.username.message}
                </small>
              )}
            </div>
          )}

          {formStep === 2 && (
            <div className="relative space-y-2">
              <label htmlFor="email" className="block text-sm text-neutral-300">
                Email
              </label>
              <input
                type="email"
                id="email"
                {...register("email")}
                placeholder="Example@email.com"
                className="w-full px-4 py-2 text-sm bg-transparent border rounded-md text-zinc-300 placeholder:text-zinc-500 focus:outline-1 border-neutral-400 focus:outline-offset-[3px] focus:ring-0"
              />
              {errors.email && (
                <small className="absolute block text-red-400">
                  {errors.email.message}
                </small>
              )}
            </div>
          )}

          {formStep === 3 && (
            <>
              <div className="mb-6 space-y-2">
                <label
                  htmlFor="password"
                  className="block text-sm text-neutral-300"
                >
                  Password
                </label>
                <input
                  type="password"
                  placeholder="Your password"
                  id="password"
                  {...register("password")}
                  className="w-full px-4 py-2 text-sm bg-transparent border rounded-md text-zinc-300 placeholder:text-zinc-400 focus:outline-1 border-neutral-400 focus:outline-offset-[3px] focus:ring-0"
                />
                {errors.password && (
                  <small className="!mt-2 text-red-400 block">
                    {errors.password.message}
                  </small>
                )}
              </div>

              <div className="space-y-2">
                <label
                  htmlFor="cPassword"
                  className="block text-sm text-neutral-300"
                >
                  Confirm Password
                </label>
                <input
                  type="password"
                  placeholder="Repeat your password"
                  id="cPassword"
                  {...register("cPassword")}
                  className="w-full px-4 py-2 text-sm bg-transparent border rounded-md text-zinc-300 placeholder:text-zinc-400 focus:outline-1 border-neutral-400 focus:outline-offset-[3px] focus:ring-0"
                />
                {errors.cPassword && (
                  <small className="!mt-2 text-red-400 block">
                    {errors.cPassword.message}
                  </small>
                )}
              </div>
            </>
          )}

          <div className="flex items-center justify-between mt-10">
            <p className="text-sm text-center text-zinc-400">
              Already have an account?{" "}
              <Link
                to="/auth/login"
                className="underline text-violet-400 hover:text-violet-500 underline-offset-2"
              >
                Login
              </Link>
            </p>

            <div className="flex gap-2">
              {formStep > 1 && (
                <button
                  type="button"
                  className="px-3 py-2 ml-auto text-sm font-semibold text-violet-400 hover:text-violet-500"
                  onClick={prevStep}
                >
                  Back
                </button>
              )}
              {formStep < 3 && (
                <button
                  type="button"
                  className="px-5 py-2 text-sm font-semibold rounded text-zinc-300 bg-violet-600 hover:bg-violet-700 disabled:bg-neutral-700 disabled:text-neutral-400 disabled:cursor-not-allowed"
                  onClick={nextStep}
                  disabled={!isStepValid()}
                >
                  Next
                </button>
              )}
              {formStep === 3 && (
                <button
                  type="submit"
                  className="py-2.5 px-5 text-sm bg-violet-700 hover:bg-violet-800 rounded-md text-violet-200 flex items-center justify-center gap-2 relative disabled:bg-neutral-700 disabled:cursor-not-allowed"
                  disabled={!isValid}
                >
                  Sign up
                </button>
              )}
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}

export default SignupPage;
