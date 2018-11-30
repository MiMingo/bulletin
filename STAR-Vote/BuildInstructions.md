cabal sandbox init
cabal install -w /opt/ghc/7.8.3/bin/ghc-7.8.3 -j ./append-only-bb/

(make sure that version 7.8.3 is the only version installed, or, specify the correct executable with -w flag)