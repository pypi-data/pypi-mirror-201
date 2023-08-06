((python-ts-mode
  . ((flymake-pyright-executable . "/home/jmunn/.nvm/versions/node/v19.7.0/bin/pyright")
     (flymake-pyright-use-poetry . nil)
     (flymake-pyright-enabled . t)
     (eglot-workspace-configuration
      . ((pylsp . ((configurationSources . ["flake8"])
                   (plugins
		    (ruff
		     (enabled . t)
		     (config . "./pyproject.toml"))
                    (flake8 (enabled . :json-false))
                    (jedi
                     (environment . "/home/jmunn/.virtualenvs/microkanren-dev"))
                    (jedi_completion
                     (enabled . t)
                     (include_params . t)
                     (include_class_objects . t)
                     (fuzzy . :json-false)
                     (eager . :json-false)
                     (resolve_at_most . 25))
                    (jedi_definition
                     (enabled . t)
                     (follow_imports . t)
                     (follow_builtin_imports . t))
                    (jedi_hover (enabled . t))
                    (jedi_references (enabled . t))
                    (jedi_signature_help (enabled . t))
                    (jedi_symbols
                     (enabled . t)
                     (all_scopes . t)
                     (include_import_symbols . t))
                    (mccabe (enabled . :json-false))
                    (preload (enabled . :json-false))
                    (preload (modules . []))
                    (pydocstyle (enabled . :json-false))
                    (pyflakes (enabled . :json-false))
                    (pylint (enabled . :json-false))
                    (rope_completion (enabled . :json-false))
                    (yapf (enabled . :json-false))
                    (pycodestyle (enabled . :json-false))
                    (pyls_isort (enabled . t))
                    (pylsp_black (enabled . t))
                    (pylsp_mypy (enabled . :json-false))))))))))
