from lib_scoring import sentencesFromSegmentations, buildSCUlist, SummaryGraph, buildSCUcandidateList
from lib_scoring import getScore, getLayerSizes, filename, processResults, scusBySentences, maxRawScore
import glob
import sys
import csv
import os

"""
============================ Input==============================
"""

summaries = list(glob.iglob('../Preprocess/peer_summaries/*'))
# See pyrmaid from "Scoring/pyrs/pyramids/" folder
pyramid = sys.argv[1]
#for testing
#pyramid = '../Scoring/pyrs/pyramids/pyramid_t77_a175_b2.0.p'
results_file = '../results.csv'
f = open(results_file, 'w')
f.close()

"""
====================== Scoring Pipeline ========================
"""

raw_scores = {}
quality_scores = {}
coverage_scores = {}
comprehension_scores = {}

print "test"
for summary in summaries:
    if os.path.isdir(summary):
        summ = glob.iglob(summary+'/*')
        for fn in summ:
            #print fn 
            #if str(fn[:-5]) == '.segs':
            if fn.endswith('.ls'):
                print "current file, ", fn
                summary_slash= fn.rfind('/') + 1
                summary_dot = fn.rfind('.')
                summary_name = fn[summary_slash:summary_dot]
                sentences = sentencesFromSegmentations(fn)
                scus = buildSCUlist(pyramid)
                Graph = SummaryGraph(sentences, scus)
                independentSet = Graph.independentSet
                candidates = buildSCUcandidateList(independentSet)
                results = processResults(candidates, independentSet)
                rearranged_results = scusBySentences(results)
                score, matched_cus = getScore(rearranged_results, scus)
                size_file = pyramid.replace('.p', '.size').replace('pyrs/pyramids/', 'sizes/')
                count_by_weight, avg = getLayerSizes(size_file)
                raw_scores[summary_name] = score
                quality = float(score)/maxRawScore(count_by_weight, matched_cus)
                coverage = float(score)/maxRawScore(count_by_weight, avg)
                comprehension = float((quality + coverage)) / 2
                quality_scores[summary_name] = quality
                coverage_scores[summary_name] = coverage
                comprehension_scores[summary_name] = comprehension
            else:
                pass

#score_tables = ['raw', 'quality', 'coverage', 'comprehension']
#scores = [raw_scores, quality_scores, coverage_scores, comprehension_scores]

with open(results_file, 'a') as f:
    w = csv.writer(f)
    w.writerow(['Summary'] + score_tables)
    for n, summary in enumerate(summaries):
    	#w.writerow([filename(summary)] + [s[n] for s in scores])
    	if os.path.isdir(summary):
            summ = glob.iglob(summary+'/*')
            for fn in summ:
                #if fn[:-5] == '.segs':
                 if fn.endswith('.ls'):
                    summary_slash= fn.rfind('/') + 1
                    summary_dot = fn.rfind('.')
                    summary_name = fn[summary_slash:summary_dot]
                    #print "Raw score for summary ", summary_name, ": ", raw_scores[summary_name]
                    output = [summary_name, raw_scores[summary_name],quality_scores[summary_name],coverage_scores[summary_name],comprehension_scores[summary_name]]
                    w.writerow(output)
                    print '{} | {:>2} | {:.3f} | {:.3f} | {:.3f}'.format("summary name", "Raw score", "Quality score", "Coverage score", "Comprehension score")
                    print '{} | {:>2} | {:.3f} | {:.3f} | {:.3f}'.format(summary_name, raw_scores[summary_name], quality_scores[summary_name],coverage_scores[summary_name],comprehension_scores[summary_name])
