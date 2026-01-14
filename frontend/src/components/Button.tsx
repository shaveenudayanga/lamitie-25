const Button = ({ children, ...props }: any) => (
  <button
    {...props}
    className=" w-full
    py-3
    rounded-xl
    font-extrabold
    tracking-widest
    uppercase
    text-yellow-300

    bg-gradient-to-r
    from-yellow-700
    via-yellow-600
    to-yellow-700

    border
    border-yellow-400/60

    shadow-lg
    shadow-yellow-500/30

    hover:from-yellow-600
    hover:via-yellow-400
    hover:to-yellow-600
    hover:shadow-yellow-400/60

    active:scale-95

    transition-all
    duration-300
    ease-out"
  >
    {children}
  </button>
);

export default Button;
