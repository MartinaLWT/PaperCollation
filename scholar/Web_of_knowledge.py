# -*- coding: utf-8 -*-
import requests
import time
from lxml import etree
import selenium
from scholar.google_settings import Settings
import re


executable_path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"


def get_html(url1):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                 "(KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"}
        r = requests.get(url1, timeout=30, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        html_text = r.text.encode("utf8")
    # print(html_text)
    except requests.exceptions.ConnectTimeout:
        html_text = ""
    return html_text


def parse_google_scholar(url1):
    essay_list = []
    html1 = get_html(url1)
    page = etree.HTML(html1)
    person_essay = page.xpath("//tr[@class='gsc_a_tr']/td[@class='gsc_a_t']/a")
    for essay in person_essay:
        essay_list.append(essay.xpath('./text()')[0])
    return essay_list


def get_webgofknowledge_info(page, title):
    names = page.xpath("//div[@class='block-record-info']/p")[0].xpath("./a/text()")
    # names_list = [names[0]]
    # for name in names[1: -1]:
    #     print(name)
    #     names_list.append(name)
    info_box = page.xpath("//div[@class='block-record-info block-record-info-source']")[0]
    try:
        publication = page.xpath("//div[@class='block-record-info']/div[contains(text(), 'Publisher')]")[0]\
            .xpath("../p/value/text()")[0]
    except IndexError:
        try:
            publication = page.xpath("//div[@class='block-record-info']/div[contains(text(), 'Publisher')]")[0] \
                .xpath("../p/text()")[0]
        except IndexError:
            publication = page.xpath("//p[@class='sourceTitle']/text()")[0]
    try:
        date = page.xpath("//div[@class='block-record-info block-record-info-source']"
                          "//span[contains(text(), 'Published:')]")[0].xpath("../value/text()")[0]
        # /../value/text()" % '出版年:')[0]
    except IndexError:
        date = page.xpath("//div[@class='block-record-info block-record-info-source']"
                          "//span[contains(text(), 'Published:')]")[0].tail
    try:
        DOI = page.xpath("//div[@class='block-record-info block-record-info-source']"
                         "//span[contains(text(), 'DOI:')]")[0].xpath("../value/text()")[0]
    except IndexError:
        DOI = ""
    try:
        essay_id = page.xpath("//div[@class='block-record-info block-record-info-source']"
                              "//span[contains(text(), 'Article Number:')]")[0].xpath("../value/text()")[0]
    except IndexError:
        essay_id = ""
    essay_type = page.xpath("//div[@class='block-record-info block-record-info-source']"
                            "//span[contains(text(), 'Document Type:')]")[0].tail
    return {"Author": names, "title": title, "published_date": date, "Publication": publication,
            "Publication search details": {"essay_id": essay_id,
                                           "DOI": DOI,
                                           "essay_type": essay_type}}


def parse_webofknowledge(essay):
    settings = Settings()
    browser = settings.browser
    # for essay in essay_list:
    browser.get("http://apps.webofknowledge.com/UA_GeneralSearch_input.do?locale=en_US&"
                "product=UA&search_mode=GeneralSearch")
        # browser.get("http://apps.webofknowledge.com/UA_GeneralSearch_input.do?"
        #             "locale=en_US&errorKey=&errorKey=&product=UA&search_mode=GeneralSearch&viewType=input")
    input_1 = browser.find_element_by_id("value(input1)")
    input_1.clear()
    input_1.send_keys(essay)
    time.sleep(1)
    browser.find_element_by_id("select2-select1-container").click()
    input_2 = browser.find_elements_by_class_name("select2-search__field")[0]
    input_2.clear()
    input_2.send_keys("title\n")
    time.sleep(5)
    browser.find_element_by_class_name("button5").click()
    time.sleep(1)
    try:
        hrefs = browser.find_elements_by_xpath("//a[@class='smallV110 snowplow-full-record']")
        for href in hrefs:
            if href.text == essay:
                href1 = href.get_attribute("href")
            if not len(hrefs):
                continue
    except selenium.common.exceptions.NoSuchElementException:
        return {"title": essay, "tag": "not found"}
    cited_times = re.findall(r"\d+", browser.find_element_by_xpath(
            "//div[@class='search-results-data-cite']").text)[0]
        # except selenium.common.exceptions.NoSuchElementException:
        # cited_times = 0
    try:
        page = etree.HTML(get_html(href1))
    except UnboundLocalError:
        return {"title": essay, "tag": "not found"}
    essay_dict = get_webgofknowledge_info(page, essay)
    essay_dict["Publication search details"]["cited_times"] = cited_times
    browser.close()
    # print(essay_dict)
    return essay_dict


def get_info_from_google_and_web_of_knowledge():
    url1 = "https://scholar.google.com.hk/citations?hl=zh-CN&user=5oGXsxUAAAAJ&pagesize=10000"
    lists = parse_google_scholar(url1)
    essay_info_list = parse_webofknowledge(lists)
    for essay_info in essay_info_list:
        print(essay_info)
    
#
# def main():
#     # url1 = "https://scholar.google.com.hk/citations?hl=zh-CN&user=5oGXsxUAAAAJ&pagesize=10000"
#     # lists = parse_google_scholar(url1)
#     lists = ['Evaluating word representation features in biomedical named entity recognition tasks',
#              'A hybrid system for temporal information extraction from clinical text',
#              'The CHEMDNER corpus of chemicals and drugs and its annotation principles',
#              'Recognizing clinical entities in hospital discharge summaries using Structural Support Vector Machines '
#              'with word representation features',
#              'A comprehensive study of named entity recognition in Chinese clinical text',
#              'Drug-Drug Interaction Extraction via Convolutional Neural Networks',
#              'Prediction of protein binding sites in protein structures using hidden Markov support vector machine',
#              'A cascade method for detecting hedges and their scope in natural language text',
#              'Answer sequence learning with neural networks for answer selection in community question answering',
#              'Clinical entity recognition using structural support vector machines with rich features',
#              'Entity recognition from clinical texts via recurrent neural network',
#              'Automatic de-identification of electronic medical records using token-level '
#              'and character-level conditional random fields',
#              'UTH_CCB: A Report for SemEval 2014–Task 7 Analysis of Clinical Text',
#              'Recognizing and Encoding Disorder Concepts in Clinical Text using Machine Learning and Vector Space Model',
#              'Overlapping community detection in networks with positive and negative links',
#              'De-identification of clinical notes via recurrent neural network and conditional random field',
#              'A comparison of conditional random fields and structured support vector machines '
#              'for chemical entity recognition in biomedical literature',
#              'Effects of semantic features on machine learning-based drug name recognition systems: '
#              'word embeddings vs. manually constructed dictionaries',
#              'Domain adaptation for semantic role labeling of clinical text',
#              'Feature engineering for drug name recognition in biomedical texts: '
#              'Feature conjunction and feature selection',
#              'Drug name recognition: approaches and resources',
#              'Overlapping community detection in weighted networks via a Bayesian approach',
#              'Network structure exploration in networks with node attributes',
#              'An automatic system to identify heart disease risk factors in clinical texts over time',
#              'Parsing clinical text: how good are the state-of-the-art parsers?',
#              'Analyzing differences between Chinese and English clinical text: '
#              'a cross-institution comparison of discharge summaries in two languages',
#              'Dependency-based convolutional neural network for drug-drug interaction extraction',
#              'A novel word embedding learning model using the dissociation between nouns and verbs',
#              'Clinical Acronym/Abbreviation Normalization using a Hybrid Approach',
#              'Investigating different syntactic context types and context representations for learning word embeddings',
#              'Validation of the ability of SYNTAX and clinical SYNTAX scores to '
#              'predict adverse cardiovascular events after stent implantation: a systematic review and meta-analysis',
#              'Role of text mining in early identification of potential drug safety issues',
#              'Recognizing disjoint clinical concepts in clinical text using machine learning-based methods',
#              'Identifying the status of genetic lesions in cancer clinical trial documents using machine learning',
#              'ICRC_HITSZ at RITE: Leveraging Multiple Classifiers Voting for Textual Entailment Recognition.',
#              'Intelligent Chinese Input Method Based on Android [J]',
#              'Chinese Word Segmentation Based on Large Margin Methods.',
#              'CNN-based ranking for biomedical entity normalization',
#              'Chinese unknown word recognition using improved conditional random fields',
#              'Incorporating Label Dependency for Answer Quality Tagging in '
#              'Community Question Answering via CNN-LSTM-CRF',
#              '语句级汉字拼音输入技术评估方法的研究',
#              'Tachycardia pacing induces myocardial neovascularization and '
#              'mobilizes circulating endothelial progenitor cells partly via SDF-1 pathway in canines',
#              'HITSZ_CNER: A hybrid system for entity recognition from Chinese clinical text',
#              'Extracting semantic lexicons from discharge summaries using machine learning and the C-Value method',
#              'HITextracter System for Chemical and Gene/Protein Entity Mention Recognition in Patents',
#              'Network structure exploration via Bayesian nonparametric models',
#              'HITSZ_CDR System for Disease and Chemical Named Entity Recognition and Relation Extraction',
#              'Identifying opinion leaders from online comments',
#              'Evaluation of Vector Space Models for Medical Disorders Information Retrieval.',
#              '置信度加权在线序列标注算法',
#              'Reranking for stacking ensemble learning',
#              'A joint syntactic and semantic dependency parsing system based on maximum entropy models',
#              'Protein Secondary Structure Prediction Using Large Margin Methods',
#              'CBN: Constructing a clinical Bayesian network based on data from the electronic medical record',
#              'Chinese Clinical Entity Recognition via Attention-Based CNN-LSTM-CRF',
#              'Recognizing continuous and discontinuous adverse drug reaction mentions from social media using LSTM-CRF',
#              'Chemical-induced disease extraction via convolutional neural networks with attention',
#              'Protein Remote Homology Detection by Combining Profile-based Protein Representation '
#              'with Local Alignment Kernel',
#              'Recognizing chemical entities in biomedical literature using conditional random fields and '
#              'structured support vector machines',
#              'Entity recognition in Chinese clinical text using attention-based CNN-LSTM-CRF',
#              'Temporal indexing of medical entity in Chinese clinical notes',
#              'LCQMC: A Large-scale Chinese Question Matching Corpus',
#              'Chemical-induced disease extraction via recurrent piecewise convolutional neural networks',
#              'Identifying High Quality Document–Summary Pairs through Text Matching',
#              '基于宏特征融合的文本分类',
#              'Icrc-dsedl: A film named entity discovery and linking system based on knowledge bases',
#              'HITSZ_CDR: an end-to-end chemical and disease relation extraction system for BioCreative V',
#              'Diversifying Question Recommendations in Community-Based Question Answering',
#              'Macro features based text categorization',
#              'Protein Remote Homology Detection and Fold Recognition based on Features Extracted '
#              'from Frequency Profiles.',
#              'KMR: knowledge-oriented medicine representation learning '
#              'for drug–drug interaction and similarity computation',
#              'A fine-grained Chinese word segmentation and part-of-speech tagging corpus for clinical text',
#              'KGDDS: A System for Drug-Drug Similarity Measure in '
#              'Therapeutic Substitution based on Knowledge Graph Curation',
#              'Drug2Vec: Knowledge-aware Feature-driven Method for Drug Representation Learning',
#              'EAPB: entropy-aware path-based metric for ontology quality',
#              'Structural regularity exploration in multidimensional networks via Bayesian inference',
#              'Usability Study of Mainstream Wearable Fitness Devices: Feature Analysis '
#              'and System Usability Scale Evaluation',
#              'The BQ Corpus: A Large-scale Domain-specific Chinese Corpus For '
#              'Sentence Semantic Equivalence Identification',
#              'Investigating Different Context Types and Representations for Learning Word Embeddings',
#              'An Initial Ingredient Analysis of Drugs Approved by China Food and Drug Administration',
#              'CMedTEX: A Rule-based Temporal Expression Extraction and Normalization System for Chinese Clinical Notes',
#              'User Recommendation Based on Network Structure in Social Networks',
#              'Structural Regularity Exploration in Multidimensional Networks',
#              'HTSZ_CEM System for Chemical Entity Mention Recognition in Patents',
#              'Automatic exploration of structural regularities in networks',
#              'ICRC_HITSZ at RITE: Leveraging Multiple Classifiers Voting for Textual Entailment Recognition',
#              'Chunking with Max-Margin Markov Networks']
#     essay_info_list = parse_webofknowledge(lists)
#     for essay_info in essay_info_list:
#         print(essay_info)
#
#
# main()

