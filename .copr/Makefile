srpm:
	dnf -y install git perl
	rpmbuild \
		--define "_sourcedir $(PWD)" \
		--define "_specdir $(PWD)" \
		--define "_rpmdir $(outdir)" \
		--define "_srcrpmdir $(outdir)" \
		-bs $(spec)
