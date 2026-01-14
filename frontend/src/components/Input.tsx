const Input = ({ className = "", ...props }: any) => (
  <input
    {...props}
    className={`
      ${className}
    `}
  />
);

export default Input;
