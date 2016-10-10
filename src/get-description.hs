#!/usr/bin/env stack
{- stack runghc --package Cabal -}

module Main where

import System.Environment (getArgs)
import Data.List
import Distribution.PackageDescription
import Distribution.PackageDescription.Parse
import qualified Distribution.ModuleName as M
import qualified Distribution.Package as P
import qualified Distribution.Verbosity as V

dependencyPackageName :: P.Dependency -> P.PackageName
dependencyPackageName (P.Dependency p _) = p

-- Outputs two lines.  The first line contains all exposed modules in the
-- package.  The second line contains all dependencies of the package.
main :: IO ()
main = do
  args <- getArgs
  desc <- case args of
            [inp] -> readPackageDescription V.normal inp
            _ -> fail "no file"
            
  let (libDeps, libModules) =
        case condLibrary desc of
          Just x -> let lib = condTreeData x
                    in (targetBuildDepends $ libBuildInfo lib,
                        exposedModules lib)
          Nothing -> ([], [])

  let exeDeps = concatMap (targetBuildDepends . buildInfo . condTreeData . snd)
                $ condExecutables desc

  let modules = map (intercalate "." . M.components) libModules
  putStrLn $ intercalate " " modules

  let dependencies = map (P.unPackageName . dependencyPackageName)
                     (libDeps ++ exeDeps)
  putStrLn $ intercalate " " dependencies
