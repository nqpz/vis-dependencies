#!/usr/bin/env stack
{- stack runghc --package Cabal -}

module Main where

import System.Environment (getArgs)
import Control.Monad
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
  let testDeps = concatMap (targetBuildDepends . testBuildInfo . condTreeData . snd)
                 $ condTestSuites desc
  let benchDeps = concatMap (targetBuildDepends . benchmarkBuildInfo . condTreeData . snd)
                  $ condBenchmarks desc

  let modules = map (intercalate "." . M.components) libModules
  putStrLn $ intercalate " " modules

  let dependenciesCore = map (P.unPackageName . dependencyPackageName)
                     (libDeps ++ exeDeps)
  let dependenciesTestBench = map (P.unPackageName . dependencyPackageName)
                     (testDeps ++ benchDeps)
  putStrLn $ intercalate " " dependenciesCore
  putStrLn $ intercalate " " dependenciesTestBench

  forM_ (sourceRepos $ packageDescription desc) $ \s -> do
    case (repoType s, repoLocation s) of
      (Just typ, Just loc) -> do
        putStrLn $ show typ
        putStrLn loc
      _ -> return ()
