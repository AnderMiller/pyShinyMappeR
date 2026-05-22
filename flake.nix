{
  description = "ShinyMappeR flake for usage and development.";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
  };

  outputs =
    { self, nixpkgs, ... }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-darwin"
      ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f system);
    in
    {
      formatter = forAllSystems (system: nixpkgs.legacyPackages.${system}.nixfmt);

      devShells = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };

          rEnv = pkgs.rWrapper.override {
            packages = with pkgs.rPackages; [
              mappeR
              ggplot2
              patchwork
              shiny
              dplyr
              tidyr
              devtools
              remotes
              RColorBrewer
              mclust
              nortest
              dendextend
              igraph
              httpuv
              styler
              lintr
              jsonlite
            ];
          };
        in
        {
          default = pkgs.mkShell {
            LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
              pkgs.stdenv.cc.cc
              pkgs.libz
              pkgs.R # rpy2 needs libR.so on LD_LIBRARY_PATH
            ];

            LC_ALL = "en_US.UTF-8";

            buildInputs = with pkgs; [
              rEnv
              pkg-config
              zlib.dev
              openssl.dev
              curl.dev
              just
              watchexec
              jq
              pyright
              python3
              ruff
              uv
              nixfmt
            ];

            shellHook = ''
              export R_LIBS_USER=""
              export R_HOME="$(R RHOME)"
              export DYLD_LIBRARY_PATH="$R_HOME/lib:$DYLD_LIBRARY_PATH"
              echo "Dev environment for ${system}..."
              echo "R: $(R --version | head -n 1)"
              echo "UV: $(uv --version)"
              echo "Python: $(python3 --version)"
              just --list-heading $'Commands:\n' \
                   --list-prefix "    just " \
                   --no-aliases --list
            '';
          };
        }
      );
    };
}
