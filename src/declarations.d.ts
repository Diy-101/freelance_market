declare namespace JSX {
  interface IntrinsicElements {
    "tgs-player": React.DetailedHTMLProps<
      React.HTMLAttributes<HTMLElement>,
      HTMLElement
    > & {
      autoplay?: boolean;
      loop?: boolean;
      mode?: string;
      src?: string;
    };
  }
}
