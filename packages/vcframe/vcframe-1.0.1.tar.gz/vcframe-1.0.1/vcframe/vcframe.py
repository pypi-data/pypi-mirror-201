import pandas as pd


class VCFrame:
    def __init__(self, metadata, data):
        self.metadata = metadata
        self.data = data
    
    def __repr__(self):
        return f'VCFrame({len(self.data)})'

    def to_vcf(self, filename):
        with open(filename, 'w+') as f:
            processed_metadata = [f'##{line}\n' for line in self.metadata]
            f.writelines(processed_metadata)
        data = self.data.copy().rename({'CHROM': '#CHROM'}, axis=1)
        data.to_csv(filename, sep='\t', mode='a', index=False)
    
    @classmethod
    def read_vcf(cls, filename):
        header = []
        skiprows = 0
        with open(filename) as f:
            for line in f.readlines():
                if line.startswith('##'):
                    processed_line = line[2:].strip()
                    header.append(processed_line)
                    skiprows += 1
                else:
                    break
        df = pd.read_csv(filename, sep='\t', skiprows=skiprows)
        df.rename({'#CHROM': 'CHROM'}, axis=1, inplace=True)
        return cls(header, df)

    def add_info(self, info):
        self.metadata.append(str(info))

