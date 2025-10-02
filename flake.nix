{
  description = "A basic flake with a shell";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.systems.url = "github:nix-systems/default";
  inputs.flake-utils = {
    url = "github:numtide/flake-utils";
    inputs.systems.follows = "systems";
  };

  outputs =
    { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells= {
          default = pkgs.mkShell { 
            buildInputs = with pkgs; [
              bashInteractive
              R 
              rPackages.mappeR 
              rPackages.shiny 
              rPackages.dendextend 
              rPackages.RColorBrewer 
              rPackages.devtools 
              rPackages.ggplot2 
            ];
          };

        # optional shell with LaTeX
          latex = pkgs.mkShell {
            buildInputs = with pkgs; [
                  bashInteractive
                  R 
                  rPackages.mappeR 
                  rPackages.shiny 
                  rPackages.dendextend 
                  rPackages.RColorBrewer 
                  rPackages.devtools 
                  rPackages.ggplot2 

                  (texlive.combine {
                    inherit (texlive)
                      scheme-medium
                      lipsum
                      latexmk
                      biblatex
                      biber
                      xetex
                      beamer;
                  })
                ];
              };
            };
          }
        );
}
