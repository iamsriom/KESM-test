#!/usr/bin/env python
import argparse
import sys
import asyncio

def main():
    parser = argparse.ArgumentParser(description="KG-RAG4SM Main2 Entry Point")
    subparsers = parser.add_subparsers(dest='command', help='Sub-commands')

    # Sub-command for similarity search
    parser_sim = subparsers.add_parser('similarity_search', help='Run similarity search')
    parser_sim.add_argument("--test_mode", action="store_true", help="Enable test mode for similarity search")

    # Sub-command for BFS paths extraction
    parser_bfs = subparsers.add_parser('bfs_paths', help='Run BFS paths extraction')
    parser_bfs.add_argument("--max_hops", type=int, default=3, help="Maximum number of hops for BFS paths")

    # Sub-command for basic BFS path ranking
    parser_rank = subparsers.add_parser('path_ranking', help='Rank BFS paths and export results')
    parser_rank.add_argument("--bfs_results", type=str, default="cms_wikidata_paths_final_full.json", help="Input BFS results JSON file")
    parser_rank.add_argument("--question_similar_data", type=str, default="cms_wikidata_similar_full.json", help="Input question similarity data JSON file")
    parser_rank.add_argument("--output_csv", type=str, default="pruned_bfs_results.csv", help="Output CSV filename")
    parser_rank.add_argument("--output_json", type=str, default="pruned_bfs_results.json", help="Output JSON filename")

    # New sub-command for triplet ranking
    parser_triplet = subparsers.add_parser('triplet_ranking', help='Run triplet ranking process')
    parser_triplet.add_argument("--synthea_parquet", type=str, default="synthea_ques_embedding_full/chroma-embeddings.parquet",
                                help="Path to the Synthea question embeddings Parquet file")
    parser_triplet.add_argument("--triplet2_dir", type=str, default="wikidata_embedding_triplet2",
                                help="Directory containing wikidata_triplet2 embeddings and metadata")
    parser_triplet.add_argument("--triplet3_dir", type=str, default="wikidata_embedding_triplet3",
                                help="Directory containing wikidata_triplet3 embeddings and metadata")
    parser_triplet.add_argument("--output_json", type=str, default="synthea_top10_similar2.json",
                                help="Output JSON file for final triplet ranking results")
    parser_triplet.add_argument("--output_excel", type=str, default="synthea_top10_similar2.xlsx",
                                help="Output Excel file for final triplet ranking results")

    args = parser.parse_args()

    if args.command == 'similarity_search':
        from modules import similarity_search
        if args.test_mode:
            sys.argv = [sys.argv[0], "--test_mode"]
        else:
            sys.argv = [sys.argv[0]]
        similarity_search.main()
    elif args.command == 'bfs_paths':
        from modules import bfs_paths
        sys.argv = [sys.argv[0], "--max_hops", str(args.max_hops)]
        asyncio.run(bfs_paths.main())
    elif args.command == 'path_ranking':
        from modules import path_ranking
        sys.argv = [sys.argv[0],
                    "--bfs_results", args.bfs_results,
                    "--question_similar_data", args.question_similar_data,
                    "--output_csv", args.output_csv,
                    "--output_json", args.output_json]
        path_ranking.main()
    elif args.command == 'triplet_ranking':
        from modules import triplet_ranking
        sys.argv = [sys.argv[0],
                    "--synthea_parquet", args.synthea_parquet,
                    "--triplet2_dir", args.triplet2_dir,
                    "--triplet3_dir", args.triplet3_dir,
                    "--output_json", args.output_json,
                    "--output_excel", args.output_excel]
        triplet_ranking.main()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
