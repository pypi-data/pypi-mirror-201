#!/usr/bin/env python3.11

import time
import asyncio
import logging

from queue import Queue

from .components.connectors import SfdcConnector
from .components.containers import ReportsContainer
from .components.handlers import WorkerFactory
from .components.config import Config
from .components.loggers import logger_configurer


def run(*,
        domain, 
        reports_path, 
        reports_list=[],
        summary_filepath="",
        log_path="", 
        report="", 
        path="", 
        threads=0, 
        stdout_loglevel="WARNING", 
        file_loglevel="WARNING", 
        verbose=False,
        ):
    """
    SFR is a simple, but very efficient due to scalability, Python application which allows you to download various reports.  
    Program supports asynchronous requests and threading for saving/processing content. Logging and CLI parameters handlig is also included.

    So far the App supports SFDC reports with SSO authentication.
    """

    t0 = time.time()

    config = Config(domain=domain,
                    reports_csv_path=reports_path,
                    reports_list=reports_list,
                    summary_filepath=summary_filepath,
                    log_path=log_path,
                    report=report, 
                    path=path, 
                    threads=threads,
                    stdout_loglevel=stdout_loglevel, 
                    file_loglevel=file_loglevel, 
                    verbose=verbose
                    )

    logger_main = logging.getLogger(__name__)
    logger_configurer(stdout_loglevel=config.stdout_loglevel,
                      file_loglevel=config.file_loglevel,
                      log_path=config.log_path,
                      verbose=config.verbose)
                      

    logger_main.info('SFR started')

    queue = Queue()    

    connector = SfdcConnector(queue, 
                              domain=config.domain,
                              verbose=config.verbose)
    connector.check_connection()
    
    container = ReportsContainer(config.report_params_list, 
                                 config.summary_filepath)
    
    WorkerFactory(queue, 
                  threads=config.threads)

    asyncio.run(connector.handle_requests(container.reports_list))

    queue.join()

    t1 = time.time()

     
    container.create_summary_report()

    container.print_summary_table()

    logger_main.info('SFR finished in %s', time.strftime(
        "%H:%M:%S", time.gmtime(t1 - t0)))
