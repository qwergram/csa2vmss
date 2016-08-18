using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace CloudServiceSeperator
{
    public partial class PreCs2Vm : Form
    {
        public PreCs2Vm()
        {
            InitializeComponent();
        }

        private void LoadCloudService(string sln_path)
        {
            LocationHintLabel.Text = sln_path;
        }

        private void SelectFolderButton_Click(object sender, EventArgs e)
        {
            OpenFileDialog SLNSelector = new OpenFileDialog();
            var SLNResult = SLNSelector.ShowDialog();
            if (SLNResult == DialogResult.OK)
            {
                this.LoadCloudService(SLNSelector.FileName);
            }
        }
    }
}
