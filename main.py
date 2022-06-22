import argparse
import data_process
import seeds_selection
import influence_count
import multiprocessing as mp
import csv
import time

def IM(path, id, policy, threshold, seed, number_of_running):
    #parser = argparse.ArgumentParser()

    #parser.add_argument('-pa', '--path', default='.\data\WS_1.txt', help='path of the graph dataset file') #单个原数据集
    #parser.add_argument('-p', '--policy', default='pagerank', help='seeds selection policy')
    #parser.add_argument('-t', '--threshold', type=float, default=1, help='propagation threshold1')
    #parser.add_argument('-s', '--seed', type=int, default=50, help='number of seed nodes ')
    #parser.add_argument('-n', '--number_of_running', type=int, default=10, help='number of running times')

    #args = parser.parse_args()
    print('Loading {} network Data...'.format(id))
    nodes, edges, target_nodes = data_process.data_load(path, id)
    #print('Done')
    #totall_influence_number = 0
    #totall_target_influence_number = 0
    #run_time = []


    #print('Generating Seeds...')
    #begin_time = time.time()
    #for i in [10, 20, 30, 40, 50]:
    result_influence_num = 0
    result_target_num = 0
    result_target_influence_radio = 0

    for k in range(10):
        totall_influence_number = 0
        totall_target_influence_number = 0
        run_time = []
        seeds_number = seed

        #print('种子节点数量为', i)
        if policy == 'degree':
            seeds = seeds_selection.degree(edges, seeds_number)
        elif policy == 'pagerank':
            seeds = seeds_selection.pagerank(nodes, edges, seeds_number)
        elif policy == 'random':
            seeds = seeds_selection.random(nodes, seeds_number)
        elif policy == 'deepwalk':
            seeds = seeds_selection.deepwalk(nodes, edges, seeds_number, target_nodes,id)
        elif policy == 'node2vec':
            seeds = seeds_selection.node2vec(nodes, edges, seeds_number, id)
        else:
            all_path = path + 'all\\' + str(id) + '.txt'
            seeds = seeds_selection.target2vec3(nodes, edges, seeds_number, target_nodes, all_path, id)

        #print('Done')
        #end_time = time.time()
        #run_time.append(end_time - begin_time)
        #print('种子节点生成时间：', run_time)
        #print('The seed nodes is {}'.format(seeds))
        #print('Calculating Influence Number...')
        for i in range(number_of_running):
            influence_number, target_influence_number = influence_count.influence_count(nodes, edges, seeds, target_nodes, threshold)
            #print('The {} iteration\'s influence number is {}'.format(i+1, influence_number))
            #print('The {} iteration\'s target influence number is {}'.format(i + 1, target_influence_number))
            totall_influence_number += influence_number
            totall_target_influence_number += target_influence_number
            #print('Done')

        #('No {} Final Average Influenced Number: {}'.format(k+1, float(totall_influence_number/number_of_running)))
        #print('No {} Final Average Target Influenced Number: {}'.format(k+1, float(totall_target_influence_number/number_of_running)))
        #print('No {} Final Target Influenced radio: {}'.format(k+1, float(totall_target_influence_number/totall_influence_number)))
        #print('Final Average Running Time: {}'.format(float(sum(run_time)/args.number_of_running)))

        result_influence_num += totall_influence_number
        result_target_num += totall_target_influence_number

    print('network {} Final Average Influenced Number: {}'.format(id, float(result_influence_num/(10*number_of_running))))
    print('network {} Final Average Target Influenced Number: {}'.format(id,float(result_target_num/(10*number_of_running))))
    print('network {} Final Target Influenced radio: {}'.format(id, float(result_target_num/result_influence_num)))

    filename = path + policy+'result.csv'
    f = open(filename, 'a', encoding='utf-8', newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow([id, float(result_influence_num/(10*number_of_running)), float(result_target_num/(10*number_of_running)), float(result_target_num/result_influence_num)])
    f.close()

def func(z):
     return IM(z[0], z[1], z[2], z[3], z[4], z[5])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-pa', '--path', default= '.\data\synthetic\BA_500_3_3\\', help='path of the graph dataset file') #单个原数据集
    parser.add_argument('-p', '--policy', default='pagerank', help='seeds selection policy')
    parser.add_argument('-t', '--threshold', type=float, default=1, help='propagation threshold1')
    parser.add_argument('-s', '--seed', type=int, default=50, help='number of seed nodes ')
    parser.add_argument('-g', '--number_of_graph', type=int, default=50, help='number of graph ')
    parser.add_argument('-n', '--number_of_running', type=int, default=10, help='number of running times')

    args = parser.parse_args()
    num_graph = args.number_of_graph
    path = args.path
    policy = args.policy
    seed = args.seed
    threshold = args.threshold
    number_of_running = args.number_of_running
    #filename = path + 'result.csv'
    #f = open(filename, 'w', encoding='utf-8', newline='')
    #csv_writer = csv.writer(f)
    #csv_writer.writerow(["ID", "totall activated", "activated target", "radio"])

    pool = mp.Pool()

    MN = [(path, id, policy, threshold, seed, number_of_running) for id in range(0, num_graph)]
    res = pool.map(func, MN)