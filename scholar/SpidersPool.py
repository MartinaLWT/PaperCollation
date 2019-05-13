import EIpart as Ei
import Web_of_knowledge as WoK
import threading
from queue import Queue


class SpiderPool:
    # from multiprocessing import Pool
    def __init__(self, func, args, thread_num=10, call_back_result=[]):
        self.work_queue = Queue()
        self.result_queue = call_back_result
        self.threads = []
        self.__init_work_queue(func, args)
        self.__init_thread_pool(thread_num)

    def __init_thread_pool(self, thread_num):
        for i in range(thread_num):
            self.threads.append(PoolWork(self.work_queue, self.result_queue))

    def __init_work_queue(self, func, args):
        for argv in args:
            self.add_job(func, argv)

    def add_job(self, func, *args):
        self.work_queue.put((func, list(args)))

    def wait_all_run(self):
        for item in self.threads:
            if item.isAlive():
                item.join()


class PoolWork(threading.Thread):
    def __init__(self, work_queue, result_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.start()

    def run(self):
        while True:
            try:
                do, args = self.work_queue.get(block=False)
                # print(zip(args))
                res = do(args[0][0], args[0][1])
                # print(do, get_url_by_image)
                self.result_queue.append(res)
                self.work_queue.task_done()
            except Exception:
                break


def get_info(url_1):
    res = WoK.parse_webofknowledge(url_1)
    if len(res) == 0:
        res = Ei.get_ei_info(url_1)
    return res


result_pool = []
essay_list = ['Evaluating word representation features in biomedical named entity recognition tasks',
             'A hybrid system for temporal information extraction from clinical text',
             'The CHEMDNER corpus of chemicals and drugs and its annotation principles',
             'Recognizing clinical entities in hospital discharge summaries using Structural Support Vector Machines '
             'with word representation features',
             'A comprehensive study of named entity recognition in Chinese clinical text',
             'Drug-Drug Interaction Extraction via Convolutional Neural Networks',
             'Prediction of protein binding sites in protein structures using hidden Markov support vector machine',
             'A cascade method for detecting hedges and their scope in natural language text',
             'Answer sequence learning with neural networks for answer selection in community question answering',
             'Clinical entity recognition using structural support vector machines with rich features',
             'Entity recognition from clinical texts via recurrent neural network',
             'Automatic de-identification of electronic medical records using token-level '
             'and character-level conditional random fields',
             'UTH_CCB: A Report for SemEval 2014–Task 7 Analysis of Clinical Text',
             'Recognizing and Encoding Disorder Concepts in Clinical Text using Machine Learning and Vector Space Model',
             'Overlapping community detection in networks with positive and negative links',
             'De-identification of clinical notes via recurrent neural network and conditional random field',
             'A comparison of conditional random fields and structured support vector machines '
             'for chemical entity recognition in biomedical literature',
             'Effects of semantic features on machine learning-based drug name recognition systems: '
             'word embeddings vs. manually constructed dictionaries',
             'Domain adaptation for semantic role labeling of clinical text',
             'Feature engineering for drug name recognition in biomedical texts: '
             'Feature conjunction and feature selection',
             'Drug name recognition: approaches and resources',
             'Overlapping community detection in weighted networks via a Bayesian approach',
             'Network structure exploration in networks with node attributes',
             'An automatic system to identify heart disease risk factors in clinical texts over time',
             'Parsing clinical text: how good are the state-of-the-art parsers?',
             'Analyzing differences between Chinese and English clinical text: '
             'a cross-institution comparison of discharge summaries in two languages',
             'Dependency-based convolutional neural network for drug-drug interaction extraction',
             'A novel word embedding learning model using the dissociation between nouns and verbs',
             'Clinical Acronym/Abbreviation Normalization using a Hybrid Approach',
             'Investigating different syntactic context types and context representations for learning word embeddings',
             'Validation of the ability of SYNTAX and clinical SYNTAX scores to '
             'predict adverse cardiovascular events after stent implantation: a systematic review and meta-analysis',
             'Role of text mining in early identification of potential drug safety issues',
             'Recognizing disjoint clinical concepts in clinical text using machine learning-based methods',
             'Identifying the status of genetic lesions in cancer clinical trial documents using machine learning',
             'ICRC_HITSZ at RITE: Leveraging Multiple Classifiers Voting for Textual Entailment Recognition.',
             'Intelligent Chinese Input Method Based on Android [J]',
             'Chinese Word Segmentation Based on Large Margin Methods.',
             'CNN-based ranking for biomedical entity normalization',
             'Chinese unknown word recognition using improved conditional random fields',
             'Incorporating Label Dependency for Answer Quality Tagging in '
             'Community Question Answering via CNN-LSTM-CRF',
             '语句级汉字拼音输入技术评估方法的研究',
             'Tachycardia pacing induces myocardial neovascularization and '
             'mobilizes circulating endothelial progenitor cells partly via SDF-1 pathway in canines',
             'HITSZ_CNER: A hybrid system for entity recognition from Chinese clinical text',
             'Extracting semantic lexicons from discharge summaries using machine learning and the C-Value method',
             'HITextracter System for Chemical and Gene/Protein Entity Mention Recognition in Patents',
             'Network structure exploration via Bayesian nonparametric models',
             'HITSZ_CDR System for Disease and Chemical Named Entity Recognition and Relation Extraction',
             'Identifying opinion leaders from online comments',
             'Evaluation of Vector Space Models for Medical Disorders Information Retrieval.',
             '置信度加权在线序列标注算法',
             'Reranking for stacking ensemble learning',
             'A joint syntactic and semantic dependency parsing system based on maximum entropy models',
             'Protein Secondary Structure Prediction Using Large Margin Methods',
             'CBN: Constructing a clinical Bayesian network based on data from the electronic medical record',
             'Chinese Clinical Entity Recognition via Attention-Based CNN-LSTM-CRF',
             'Recognizing continuous and discontinuous adverse drug reaction mentions from social media using LSTM-CRF',
             'Chemical-induced disease extraction via convolutional neural networks with attention',
             'Protein Remote Homology Detection by Combining Profile-based Protein Representation '
             'with Local Alignment Kernel',
             'Recognizing chemical entities in biomedical literature using conditional random fields and '
             'structured support vector machines',
             'Entity recognition in Chinese clinical text using attention-based CNN-LSTM-CRF',
             'Temporal indexing of medical entity in Chinese clinical notes',
             'LCQMC: A Large-scale Chinese Question Matching Corpus',
             'Chemical-induced disease extraction via recurrent piecewise convolutional neural networks',
             'Identifying High Quality Document–Summary Pairs through Text Matching',
             '基于宏特征融合的文本分类',
             'Icrc-dsedl: A film named entity discovery and linking system based on knowledge bases',
             'HITSZ_CDR: an end-to-end chemical and disease relation extraction system for BioCreative V',
             'Diversifying Question Recommendations in Community-Based Question Answering',
             'Macro features based text categorization',
             'Protein Remote Homology Detection and Fold Recognition based on Features Extracted '
             'from Frequency Profiles.',
             'KMR: knowledge-oriented medicine representation learning '
             'for drug–drug interaction and similarity computation',
             'A fine-grained Chinese word segmentation and part-of-speech tagging corpus for clinical text',
             'KGDDS: A System for Drug-Drug Similarity Measure in '
             'Therapeutic Substitution based on Knowledge Graph Curation',
             'Drug2Vec: Knowledge-aware Feature-driven Method for Drug Representation Learning',
             'EAPB: entropy-aware path-based metric for ontology quality',
             'Structural regularity exploration in multidimensional networks via Bayesian inference',
             'Usability Study of Mainstream Wearable Fitness Devices: Feature Analysis '
             'and System Usability Scale Evaluation',
             'The BQ Corpus: A Large-scale Domain-specific Chinese Corpus For '
             'Sentence Semantic Equivalence Identification',
             'Investigating Different Context Types and Representations for Learning Word Embeddings',
             'An Initial Ingredient Analysis of Drugs Approved by China Food and Drug Administration',
             'CMedTEX: A Rule-based Temporal Expression Extraction and Normalization System for Chinese Clinical Notes',
             'User Recommendation Based on Network Structure in Social Networks',
             'Structural Regularity Exploration in Multidimensional Networks',
             'HTSZ_CEM System for Chemical Entity Mention Recognition in Patents',
             'Automatic exploration of structural regularities in networks',
             'ICRC_HITSZ at RITE: Leveraging Multiple Classifiers Voting for Textual Entailment Recognition',
             'Chunking with Max-Margin Markov Networks']


def spider_pool_run(url_1):
    # essay_list = Google.get_info_from_google(url_1)

    max_pool = SpiderPool(get_info, essay_list, call_back_result=result_pool)
    max_pool.wait_all_run()
    print(result_pool)


spider_pool_run("https://scholar.google.com.hk/citations?hl=zh-CN&user=5oGXsxUAAAAJ")

