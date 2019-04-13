#include <iostream>
#include <string>
#include <fstream>
#include <unordered_map>
#include <map>
#include <unordered_set>
#include <queue>

// std::string find_node_id(const std::string &year, const std::string &filename,
//    std::queue<std::string> &q, bool flag = false);
std::multimap<int,int> partition_edges(const std::string &filename, const size_t min_out_deg);

// void put_next_500(std::queue<std::string> &q, size_t low_bnd, size_t up_bnd, 
//    const std::multimap<int,int> &future);

int main(int argc, char const *argv[])
{
   if(argc != 3)
   {
      std::cerr << "Expected 3 argument arguments: received: " << argc << std::endl;
      std::cerr << "Provide arguments in following order: " << 
         "1) ./executable "
         "2) Edge list file name " 
         "3) Min out degree"
         // "3) Node info file name "
         // "4) Input year (lower) to partition"
         // "5) Input year (upper) to partition"
         // "6) Get_next_500 (boolean: true if getting next 500; false if not)"
         << std::endl;
      exit(EXIT_FAILURE);
   }

   std::string edge_filename(argv[1]);
   auto min_out_deg = std::stoi(argv[2]);
   // std::string node_info_filename(argv[2]);
   // std::string year_lower(argv[3]);
   // std::string year_upper(argv[4]);

   std::cout << "---------------INPUT PARAMETERS-------------------------" << std::endl;
   std::cout << "Connectivity input file name: " << edge_filename << std::endl;
   std::cout << "Min out degree: " << min_out_deg << std::endl;
   // std::cout << "Year lower input: " << year_lower << std::endl;
   // std::cout << "Year upper input: " << year_upper << std::endl;
   std::cout << "--------------------------------------------------------" << std::endl;

   // std::queue<std::string> q;
   // auto lower_node_id = find_node_id(year_lower, node_info_filename, q);
   // auto upper_node_id = find_node_id(year_upper, node_info_filename, q, true);
   // std::cout << q.size() << std::endl;

   // auto future = partition_edges(std::stoi(lower_node_id), std::stoi(upper_node_id), edge_filename);
   auto future = partition_edges(edge_filename, min_out_deg);

   // std::cout << future.size() << std::endl;
   // if(argv[5] == "true") put_next_500(q, std::stoi(lower_node_id), std::stoi(upper_node_id), future);

   return 0;
}

// void put_next_500(std::queue<std::string> &q, size_t low_bnd, size_t up_bnd, 
//    const std::multimap<int,int> &future)
// {
//    std::ofstream trainfile("subgraph.txt", std::ios_base::app);
//    if(!trainfile)
//    {
//       std::cerr << "Unable to open " << "subgraph.txt" << std::endl;
//       std::cerr << "Exiting.." << std::endl;
//       exit(EXIT_FAILURE);
//    }

//    std::string u, v;
//    //u is citing and v is cited
//    //we need to check if the front of the q exists in the first column. If it doesn't exist
//    //then we throw it out. If it exists, then we need to check if the value is < up_bnd. If it's not
//    //we throw it out
//    //Otherwise we
//    //add this popped value to our hash table upt o date. The trick is there can be multiple key-value
//    //pairs with the same key
//    size_t counter = 0;
//    size_t popped;
//    std::unordered_set<size_t> future500;
//    while(!q.empty() && counter < 500)
//    {
//       popped = std::stoi(q.front());
//       q.pop();

//       if(future.find(popped) != future.end())
//       {
//          auto my_pair = future.equal_range(popped);

//          if(std::distance(my_pair.first, my_pair.second) >= 2)//we only want nodes that have 2 or more edges
//          {  
//             auto not_found = true;

//             for(auto it = my_pair.first; it != my_pair.second; it++)
//             {
//                if(it->second < up_bnd && future500.find(it->second) == future500.end()){}
//                else not_found = false;
//             }

//             if(not_found)
//             {
//                for(auto it = my_pair.first; it != my_pair.second; it++)
//                {
//                   future500.emplace(popped);
//                   trainfile << it->first << " " << it->second << std::endl;
//                }            
//                counter++;
//             }
//          }
//       }
//       // else std::cout << "popped not found; this shouldn't happen; node id is: " << popped << std::endl;

//    }
// }

//function for partioning the provide edge list file into train and test data based on node_id
// std::multimap<int,int> partition_edges(const int low_bnd, const int up_bnd, const std::string &filename)
std::multimap<int,int> partition_edges(const std::string &filename, const size_t min_out_deg)
{
   const std::string subgraph_filename("subgraph.txt");
   // const std::string test_filename("test.dat");
   std::multimap<int,int> future;
   std::unordered_map<int, std::vector<int> > adj_list;

   std::cout << "Partioning edges into train and test.." << std::endl;

   std::ifstream infile;
   infile.open(filename);

   if(!infile)
   {
      std::cerr << "Unable to open " << filename << std::endl;
      std::cerr << "Exiting.." << std::endl;
      exit(EXIT_FAILURE);
   }

   std::string str;
   bool found_numeric = false;
   int i = 0;
   while(!found_numeric)
   {
      std::getline(infile, str, '\n');

      if(!str.find("#")) continue;     //skips the header lines begining with a #, modify later
      else found_numeric = true;
   }
   std::cout << "here"<< std::endl;

   auto u = std::stoi(str.substr(0, str.find(' ')));     //cit-Patents.txt uses tabs -.-
   auto v = std::stoi(str.substr(str.find(' ')));

   // if(u < up_bnd && v < up_bnd && u >= low_bnd && v >= low_bnd) adj_list.emplace(u,v);
   // else if(u >= up_bnd && v >= low_bnd) future.emplace(u,v); 
   adj_list[u] = {v};

   int counter = 0;
   while(infile >> u >> v)
   {
      counter++;
      if(counter % 1000 == 0)
         std::cout << counter << std::endl;
      if(adj_list.find(u) == adj_list.end()) adj_list[u] = {v};
      else adj_list[u].emplace_back(v);
      // if(u < up_bnd && v < up_bnd && u >= low_bnd && v >= low_bnd) trainfile << u << " " << v << std::endl;
      // else if(u >= up_bnd && v >= low_bnd) future.emplace(u,v); 
   }

   infile.close();
   std::cout << "Finished parsing edge file" << std::endl;

   std::ofstream subgraphfile(subgraph_filename);
   for(const auto &ht_element : adj_list)
   {
      size_t num_ele = ht_element.second.size();
      if(num_ele >= min_out_deg)
      {
         for(const auto &val : ht_element.second)
         {
            if(adj_list[val].size() > 1)
               subgraphfile << ht_element.first << " " << val << std::endl;
         }
      }
   }


   subgraphfile.close();


   std::cout << "Partitioning done." << std::endl;

   return future; 
}

// std::string find_node_id(const std::string &year, const std::string &filename, 
//    std::queue<std::string> &q, bool flag)
// {
//    std::cout << "Finding first node id corresponding to input year" << std::endl;

//    std::ifstream infile(filename);

//    if(!infile)
//    {
//       std::cerr << "Unable to open " << filename << std::endl;
//       std::cerr << "Exiting.." << std::endl;
//       exit(EXIT_FAILURE);
//    }

//    std::string node_id = "-1";
//    std::string str;

//    int i = 0;

//    while(node_id == "-1" && std::getline(infile, str, '\n'))
//    {
//       if(!str.find("\"")) continue;     //skips the header lines begining with a quote, modify later

//       auto pos = str.find(',');

//       if(!str.substr(pos + 1).find(year))   //find node_id corresponding to provided year
//       {
//          node_id = str.substr(0,pos);
//       }
//    }

//    //now store the next nodes for future link prediction
//    if(flag)
//    {
//       q.emplace(node_id);         
//       while(std::getline(infile, str, '\n'))
//       {
//          if(!str.find("\"")) continue;     //skips the header lines begining with a quote, modify later

//          auto pos = str.find(',');
//          pos = std::min(pos, str.find(' '));
//          pos = std::min(pos, str.find('\t'));
//          q.emplace(str.substr(0, pos));
//       }
//    }

//    infile.close();

//    if(node_id == "-1")
//    {
//       std::cerr << "Year not found! Exiting.." << std::endl;
//       exit(EXIT_FAILURE);
//    }

//    std::cout << "Found first node id corresponding to year " << year << ": " << node_id << std::endl;

//    return node_id;
// }
