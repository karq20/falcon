"""
Multithreading
	- use ProcessPoolExecutor for CPU bound operations
	- use ThreadPoolExecutor for I/O bound operations

P.S. Running OCR is a CPU bound activity
"""

import concurrent.futures
import text_with_confidence

def process(image_list, no_of_proc):
    futures = []
    results = []
    if no_of_proc is None:
        no_of_proc = 4

    """ Executor Submit - Returns whatever is done, 9 sec """
    executor = concurrent.futures.ProcessPoolExecutor(no_of_proc)
    for image_obj in image_list:
    	futures.append(executor.submit(text_with_confidence.do, image_obj["image"], image_obj["rgb"], image_obj["conf"]))

    for r in concurrent.futures.as_completed(futures):
        results.append(r.result())

    """ Executor Map - Returns in order of input, 9 sec """
    # executor = concurrent.futures.ProcessPoolExecutor(4)
    # futures = executor.map(runocr, image_list)
    # for r in futures:
    # 	print(r)

    return results
