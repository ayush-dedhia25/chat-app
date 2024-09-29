import { yupResolver } from "@hookform/resolvers/yup";
import { useForm } from "react-hook-form";
import { Link } from "react-router-dom";
import * as Yup from "yup";

import useAuth from "../../hooks/useAuth";

const validationSchema = Yup.object().shape({
  usernameOrEmail: Yup.string().required("Email or username is required"),
  password: Yup.string().required("Password is required"),
});

function LoginPage() {
  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm({
    resolver: yupResolver(validationSchema),
  });
  const { login } = useAuth();

  const handleLogin = async (data) => {
    try {
      await login(data);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="flex items-center justify-center flex-1">
      <div className="w-[60%] flex flex-col gap-6">
        <div className="flex flex-col items-center">
          <h2 className="text-2xl font-bold text-violet-300">
            Welcome Back to Textify! 👋🏻
          </h2>
          <p className="mt-3 text-sm text-center text-neutral-300">
            Ready to connect? {"Let's"} make today unforgettable. Sign in to chat with
            your friends and family, and stay in the loop!
          </p>
        </div>

        <form className="space-y-5" onSubmit={handleSubmit(handleLogin)}>
          <div className="space-y-2">
            <label htmlFor="usernameOrEmail" className="block text-sm text-neutral-300">
              Email or Username
            </label>
            <input
              type="text"
              id="usernameOrEmail"
              {...register("usernameOrEmail")}
              placeholder="Login with username or email"
              className="w-full px-4 py-2 text-sm bg-transparent border rounded-md text-zinc-300 placeholder:text-zinc-400 focus:outline-1 border-neutral-400 focus:outline-offset-[3px] focus:ring-0"
            />
            {errors.usernameOrEmail && (
              <small className="!mt-2 text-red-400 block">
                {errors.usernameOrEmail.message}
              </small>
            )}
          </div>

          <div className="space-y-2">
            <label htmlFor="password" className="block text-sm text-neutral-300">
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

          <Link to="#" className="block text-sm text-right text-violet-400">
            Forgot password?
          </Link>

          <button
            type="submit"
            className="w-full py-2.5 bg-violet-700 hover:bg-violet-800 rounded-md text-violet-200 flex items-center justify-center gap-2 relative disabled:bg-neutral-700 disabled:cursor-not-allowed disabled:text-neutral-500 !mt-3"
            disabled={!isValid}
          >
            Sign in
          </button>
        </form>

        <p className="text-sm text-center text-zinc-400">
          {"Don't"} you have an account?{" "}
          <Link
            to="/auth/sign-up"
            className="underline text-violet-400 underline-offset-2"
          >
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;
